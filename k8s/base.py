#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2019 The FIAAS Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from abc import ABC

import json
import logging
from collections import namedtuple
from typing import Optional, Dict, List

import requests
import requests.packages.urllib3 as urllib3

from . import config
from .client import Client, NotFound
from .fields import Field

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class MetaModel(type):
    """Metaclass for Model

    Responsibilities:

    * Creating the _meta attribute, with url_template (if present), list of fields
      and for convenience, a list of field names.
    * Creates properties for name and namespace if the instance has a metadata field.
    * Mixes in ApiMixIn if the Model has a Meta attribute, indicating a top level
      Model (not to be confused with _meta).
    """

    @staticmethod
    def __new__(mcs, cls, bases, attrs):
        attr_meta = attrs.pop("Meta", None)
        if attr_meta:
            bases += (ApiMixIn,)
        meta = {
            "url_template": getattr(attr_meta, "url_template", ""),
            "list_url": getattr(attr_meta, "list_url", ""),
            "watch_list_url": getattr(attr_meta, "watch_list_url", ""),
            "watch_list_url_template": getattr(attr_meta, "watch_list_url_template", ""),
            "fields": [],
            "field_names": [],
        }
        field_names = meta["field_names"]
        fields = meta["fields"]
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                if v.name == "__unset__":
                    v.name = k
                v.attr_name = k
                field_names.append(k)
                fields.append(v)
        Meta = namedtuple("Meta", meta.keys())
        attrs["_meta"] = Meta(**meta)
        return super(MetaModel, mcs).__new__(mcs, cls, bases, attrs)


class ApiMixIn(object):
    """ApiMixIn class for top level Models

    Contains methods for working with the API
    """

    _client = Client()

    @classmethod
    def _build_url(cls, **kwargs):
        return cls._meta.url_template.format(**kwargs)

    @classmethod
    def find(cls, name="", namespace="default", labels=None):
        """Find resources using label selection

        :param: :py:class:`str` name: The name of the resource, as indicated by the `app` label
        :param: :py:class:`str` namespace: The namespace to search in
        :param: :py:class:`dict` labels: More advanced label selection (see below)

        :returns: A list of matching objects

        When a `labels` dictionary is supplied, the `name` parameter is ignored.
        See the docs for _label_selector for more details
        """
        if namespace is None:
            if not cls._meta.list_url:
                raise NotImplementedError("Cannot find without namespace, no list_url defined on class {}".format(cls))
            url = cls._meta.list_url
        else:
            url = cls._build_url(name="", namespace=namespace)
        if not labels:
            labels = {"app": Equality(name)}
        selector = cls._label_selector(labels)
        resp = cls._client.get(url, params={"labelSelector": selector})
        return [cls.from_dict(item) for item in resp.json()["items"]]

    @classmethod
    def _list_raw(cls, namespace="default"):
        """List all resources in given namespace"""
        if namespace is None:
            if not cls._meta.list_url:
                raise NotImplementedError("Cannot list without namespace, no list_url defined on class {}".format(cls))
            url = cls._meta.list_url
        else:
            url = cls._build_url(name="", namespace=namespace)
        resp = cls._client.get(url)
        return resp

    @classmethod
    def list(cls, namespace="default"):
        """List all resources in given namespace"""
        resp = cls._list_raw(namespace=namespace)
        return [cls.from_dict(item) for item in resp.json()["items"]]

    @classmethod
    def list_with_meta(cls, namespace="default"):
        """List all resources in given namespace. Return ModelList"""
        resp = cls._list_raw(namespace=namespace)
        return ModelList.from_dict(cls, resp.json())

    @classmethod
    def watch_list(cls, namespace=None, resource_version=None, allow_bookmarks=False):
        """Return a generator that yields WatchEvents of cls.
        If allowBookmarks is True, WatchBookmarks will also be yielded.
        It's recommended to use the Watcher class instead of calling this directly,
        since it handles reconnects and resource versions.
        """
        url = cls._watch_list_url(namespace)

        # We don't pass timeoutSeconds to the server, since our timeout is between each event,
        # while the server will apply the timeout as a maximum time serving the full request,
        # hanging up regardless of time between events. Let the server decide that timeout.
        params = {}
        if resource_version:
            # As per https://kubernetes.io/docs/reference/using-api/api-concepts/#semantics-for-watch
            # only resourceVersion is used for watch queries.
            params["resourceVersion"] = resource_version
            LOG.info("(Re)starting %s watch at resource version %s", cls.__name__, resource_version)
        if allow_bookmarks:
            params["allowWatchBookmarks"] = "true"

        try:
            # The timeout here appears to be per call to the poll (or similar) system call,
            # so each time data is received, the timeout will reset.
            resp = cls._client.get(url, stream=True, timeout=config.stream_timeout, params=params)
            for line in resp.iter_lines(chunk_size=None):
                event = cls._parse_watch_event(line) if line else None
                if event:
                    yield event
        except requests.ConnectionError as e:
            # ConnectionError is fairly generic, but check for ReadTimeoutError from urllib3.
            # If we get this, there were no events received for the timeout period, which might not be an error,
            # just a quiet period.
            underlying = e.args[0]
            if isinstance(underlying, urllib3.exceptions.ReadTimeoutError):
                LOG.info(
                    "Read timeout while waiting for new %s events.",
                    cls.__name__,
                )
                return
            raise

    @classmethod
    def _watch_list_url(cls, namespace):
        """Loads the optionally namespaced url from the class meta"""
        if namespace:
            if cls._meta.watch_list_url_template:
                url = cls._meta.watch_list_url_template.format(namespace=namespace)
            else:
                raise NotImplementedError(
                    "Cannot watch_list with namespace, no watch_list_url_template defined on class {}".format(cls)
                )
        else:
            url = cls._meta.watch_list_url
            if not url:
                raise NotImplementedError("Cannot watch_list, no watch_list_url defined on class {}".format(cls))
        return url

    @classmethod
    def _parse_watch_event(cls, line) -> Optional[WatchBaseEvent]:
        """
        Parse a line from the watch stream into a WatchEvent or WatchBookmark.
        Raises APIServerError if the line is an error event.
        """
        try:
            event_json = json.loads(line)
            if APIServerError.match(event_json):
                err = APIServerError(event_json["object"])
                LOG.warning(
                    "Received error event from API server: %s",
                    err,
                )
                raise err
            if WatchBookmark.match(event_json):
                LOG.debug("Received bookmark from API server: %s", event_json)
                event = WatchBookmark(event_json)
            else:
                LOG.debug("Received watch event from API server: %s", event_json)
                event = WatchEvent(event_json, cls)
            return event
        except TypeError:
            LOG.exception(
                "Unable to create instance of %s from watch event json, discarding event. event_json=%r",
                cls.__name__,
                event_json,
            )
        except ValueError:
            LOG.exception(
                "Unable to parse JSON on watch event, discarding event. Line: %r",
                line,
            )
        return None

    @classmethod
    def get(cls, name, namespace="default"):
        """Get from API server if it exists"""
        url = cls._build_url(name=name, namespace=namespace)
        resp = cls._client.get(url)
        instance = cls.from_dict(resp.json())
        return instance

    @classmethod
    def get_or_create(cls, **kwargs):
        """If exists, get from API, else create new instance"""
        try:
            metadata = kwargs.get("metadata")
            instance = cls.get(metadata.name, metadata.namespace)
            for field in cls._meta.fields:
                field.set(instance, kwargs)
            return instance
        except NotFound:
            return cls(new=True, **kwargs)

    @classmethod
    def delete(cls, name, namespace="default", **kwargs):
        """Delete the named resource"""
        url = cls._build_url(name=name, namespace=namespace)
        cls._client.delete(url, **kwargs)

    @classmethod
    def delete_list(cls, namespace="default", labels=None, delete_options=None, **kwargs):
        selector = cls._label_selector(labels)
        url = cls._build_url(name="", namespace=namespace)
        if delete_options:
            delete_options = delete_options.as_dict()

        cls._client.delete(url, body=delete_options, params={"labelSelector": selector}, **kwargs)

    def save(self):
        """Save to API server, either update if existing, or create if new"""
        if self._new:
            url = self._build_url(name="", namespace=self.metadata.namespace)
            resp = self._client.post(url, self.as_dict())
            self._new = False
        else:
            url = self._build_url(name=self.metadata.name, namespace=self.metadata.namespace)
            resp = self._client.put(url, self.as_dict())
        self.update_from_dict(resp.json())

    def save_status(self):
        """Save status to API server, always updating"""
        url = self._build_url(name=self.metadata.name, namespace=self.metadata.namespace) + "/status"
        resp = self._client.put(url, self.as_dict())
        self.update_from_dict(resp.json())

    @staticmethod
    def _label_selector(labels):
        """Build a labelSelector string from a collection of key/values. The parameter can be either
        a dict, or a list of (key, value) tuples (this allows for repeating a key).

        The keys/values are used to build the `labelSelector` parameter to the API,
        and supports all the operations of the API through the use of :py:class:`~k8s.base.LabelSelector`.

        Each key is a label name. The value defines which operation to perform.
        Operations that take a single string value:

            - :py:class:`~k8s.base.Equality`
            - :py:class:`~k8s.base.Inequality`

        A plain string will automatically be wrapped by :py:class:`~k8s.base.Equality` for compatability
        with older versions of this method.

        Operations that take a sequence of string values:

            - :py:class:`~k8s.base.In`
            - :py:class:`~k8s.base.NotIn`

        Operations that takes no value:

            - :py:class:`~k8s.base.Exists`
        """

        if hasattr(labels, "items"):
            labels = sorted(labels.items(), key=lambda kv: kv[0])

        return ",".join("{}{}".format(k, v if isinstance(v, LabelSelector) else Equality(v)) for k, v in labels)


class Model(metaclass=MetaModel):
    """A kubernetes Model object

    Contains fields for each attribute in the API specification, and methods for export/import.
    """

    def __init__(self, new=True, **kwargs):
        self._new = new
        self._values = {}
        kwarg_names = set(kwargs.keys())
        for field in self._meta.fields:
            kwarg_names.discard(field.name)
            field.set(self, kwargs)
            if field.type == SelfModel:
                field.type = self.__class__
                field.default_value_create_instance = False
        if kwarg_names:
            raise TypeError(
                "{}() got unexpected keyword-arguments: {}".format(self.__class__.__name__, ", ".join(kwarg_names))
            )
        if self._new:
            self._validate_fields()

    def _validate_fields(self):
        for field in self._meta.fields:
            if not field.is_valid(self):
                raise TypeError("Value of field {} is not valid on {}".format(field.name, self))

    def as_dict(self):
        if all(getattr(self, field.attr_name) == field.default_value for field in self._meta.fields):
            return None
        d = {}
        for field in self._meta.fields:
            value = field.dump(self)
            if value is not None:
                d[_api_name(field.name)] = value
        return d

    def merge(self, other):
        """
        `merge` sets each field in `self` to the value provided by `other`
        This is mostly equivalent to just replacing `self` with `other`,
        except read only fields in `self` are preserved.
        """
        for field in self._meta.fields:
            setattr(self, field.name, getattr(other, field.name))

    update = merge  # For backwards compatibility

    def update_from_dict(self, d):
        for field in self._meta.fields:
            field.load(self, d.get(_api_name(field.name)))
        self._validate_fields()

    @classmethod
    def from_dict(cls, d):
        instance = cls(new=False)
        instance.update_from_dict(d)
        return instance

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={}".format(key, getattr(self, key)) for key in self._meta.field_names),
        )

    def __eq__(self, other):
        try:
            return self.as_dict() == other.as_dict()
        except AttributeError:
            return False


def _api_name(name):
    return name[1:] if name.startswith("_") else name


class WatchBaseEvent(ABC):
    """Abstract base class for Watch events.
    Contains the resource version of the event as property resource_version."""

    __slots__ = ("resource_version",)

    def __init__(self, event_json=None, resource_version=None):
        if event_json is not None:
            self.resource_version = event_json["object"].get("metadata", {}).get("resourceVersion")
        else:
            self.resource_version = resource_version

    def __eq__(self, other):
        return self.resource_version == other.resource_version

    def has_object(self):
        ...


class WatchEvent(WatchBaseEvent):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"

    def __init__(self, event_json: dict = None, cls: type[Model] = None, _type: str = None, _object: Model = None):
        if event_json is not None and cls is not None:
            super(WatchEvent, self).__init__(event_json=event_json)
            self.type = event_json["type"]
            self.object = cls.from_dict(event_json["object"])
        elif _type is not None and _object is not None:
            # resource_version is effectively optional here to match the behavior for event_json in WatchBaseEvent
            # in practice, watch events with None resourceVersion will break the caching in Watcher.watch()
            resource_version = getattr(getattr(_object, "metadata", None), "resourceVersion", None)
            super(WatchEvent, self).__init__(resource_version=resource_version)
            self.type = _type
            self.object = _object
        else:
            raise ValueError("requires either event_json and cls or _type and _object, " +
                             f"got {event_json=}, {cls=}, {_type=}, {_object=}")

    def __repr__(self):
        return "{cls}(type={type}, object={object})".format(
            cls=self.__class__.__name__, type=self.type, object=self.object
        )

    def __eq__(self, other):
        return self.type == other.type and self.object == other.object

    def has_object(self):
        return True


class SyntheticAddedWatchEvent(WatchEvent):
    def __init__(self, obj: Model):
        super(SyntheticAddedWatchEvent, self).__init__(_type=WatchEvent.ADDED, _object=obj)


class WatchBookmark(WatchBaseEvent):
    """Bookmark events, if enabled, are sent periodically by the API server.
    They only contain the resourceVersion of the event."""

    def __init__(self, event_json):
        super(WatchBookmark, self).__init__(event_json)

    @classmethod
    def match(cls, event_json):
        return event_json["type"] == "BOOKMARK"

    def has_object(self):
        return False


class LabelSelector(object):
    """Base for label select operations"""

    #: Operator used in selection query
    operator = None

    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return "{}{}".format(self.operator, self.value)


class Equality(LabelSelector):
    operator = "="


class Inequality(LabelSelector):
    operator = "!="


class LabelSetSelector(LabelSelector):
    def __str__(self):
        return " {} ({})".format(self.operator, ",".join(self.value))


class In(LabelSetSelector):
    operator = "in"


class NotIn(LabelSetSelector):
    operator = "notin"


class Exists(LabelSelector):
    def __init__(self):
        super(Exists, self).__init__("")

    def __str__(self):
        return ""


class SelfModel:
    """
    Use `SelfModel` as `Field.type` to set `Field.type` to the model the
    `Field` was defined in during model instantiation.

    This allows models to have fields with their own type.
    It is not possible to reference a class in its own attributes.

    Example:
    ```
    class MyModel(Model):
        submodel = Field(SelfModel) # submodel gets the type `MyModel`
    ```
    """

    pass


class APIServerError(Exception):
    """Raised when the API server returns an error event in the watch stream"""

    def __init__(self, api_error):
        self.api_error = api_error

    def __str__(self):
        code = self.api_error["code"]
        reason = self.api_error.get("reason", "(unset)")
        message = self.api_error.get("message", "(unset)")
        return f"{code}: reason={reason} message={message}"

    @classmethod
    def match(cls, event_json):
        return event_json["type"] == "ERROR" and event_json["object"].get("kind") == "Status"


class ListMeta(Model):
    _continue = Field(str)
    remainingItemCount = Field(int)
    resourceVersion = Field(str)


class ModelList:
    """
    Generic type to hold list of Model instances (items) together with ListMeta (metadata),
    as returned by list API calls
    """

    def __init__(self, metadata: ListMeta, items: List[Model]):
        self.metadata = metadata
        self.items = items

    @classmethod
    def from_dict(cls, model_cls: type[Model], list_response_data: Dict):
        metadata = ListMeta.from_dict(list_response_data.get('metadata', {}))
        items = [model_cls.from_dict(item) for item in list_response_data.get('items', [])]
        return cls(metadata, items)
