#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import json
import logging
from collections import namedtuple

import six

from .client import Client, NotFound
from .fields import Field

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

URL_FIELDS = (
    "create_url",
    "delete_url",
    "get_url",
    "update_url",
    "list_all_url",
    "list_ns_url",
    "watch_url",
    "watchlist_all_url",
    "watchlist_ns_url",
)


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
            "fields": [],
            "field_names": []
        }
        for url_field in URL_FIELDS:
            meta[url_field] = getattr(attr_meta, url_field, "")
        field_names = meta["field_names"]
        fields = meta["fields"]
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                v.name = k
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
    def find(cls, name, namespace="default", labels=None):
        if namespace is None:
            url = cls._meta.list_all_url
        else:
            url = cls._meta.list_ns_url.format(namespace=namespace)
        if not url:
            raise NotImplementedError("No URL defined for find on {}".format(cls.__name__))
        if labels:
            selector = ",".join("{}={}".format(k, v) for k, v in labels.items())
        else:
            selector = "app={}".format(name)
        resp = cls._client.get(url, params={"labelSelector": selector})
        return [cls.from_dict(item) for item in resp.json()[u"items"]]

    @classmethod
    def list(cls, namespace="default"):
        if namespace is None:
            url = cls._meta.list_all_url
        else:
            url = cls._meta.list_ns_url.format(namespace=namespace)
        if not url:
            raise NotImplementedError("No URL defined for list on {}".format(cls.__name__))
        resp = cls._client.get(url)
        return [cls.from_dict(item) for item in resp.json()[u"items"]]

    @classmethod
    def watch_list(cls, namespace=None):
        """Return a generator that yields WatchEvents of cls"""
        if namespace:
            url = cls._meta.watchlist_ns_url.format(namespace=namespace)
        else:
            url = cls._meta.watchlist_all_url
        if not url:
            raise NotImplementedError("No URL defined for watch_list on {}".format(cls.__name__))
        for event in cls._watch(url):
            yield event

    @classmethod
    def watch(cls, name, namespace="default"):
        url = cls._meta.watch_url.format(name=name, namespace=namespace)
        if not url:
            raise NotImplementedError("No URL defined for watch on {}".format(cls.__name__))
        for event in cls._watch(url):
            yield event

    @classmethod
    def _watch(cls, url):
        resp = cls._client.get(url, stream=True, timeout=None)
        for line in resp.iter_lines(chunk_size=None):
            if line:
                try:
                    event_json = json.loads(line)
                    event = WatchEvent(event_json, cls)
                    yield event
                except ValueError:
                    LOG.exception("Unable to parse JSON on watch event, discarding event. Line: %r", line)

    @classmethod
    def get(cls, name, namespace="default"):
        """Get from API server if it exists"""
        url = cls._meta.get_url.format(name=name, namespace=namespace)
        if not url:
            raise NotImplementedError("No URL defined for get on {}".format(cls.__name__))
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
        url = cls._meta.delete_url.format(name=name, namespace=namespace)
        if not url:
            raise NotImplementedError("No URL defined for delete on {}".format(cls.__name__))
        cls._client.delete(url, **kwargs)

    def save(self):
        """Save to API server, either update if existing, or create if new"""
        if self._new:
            url = self._meta.create_url.format(namespace=self.metadata.namespace)
            if not url:
                raise NotImplementedError("No URL defined for save on {}".format(self.__class__.__name__))
            resp = self._client.post(url, self.as_dict())
            self._new = False
        else:
            url = self._meta.update_url.format(name=self.metadata.name, namespace=self.metadata.namespace)
            if not url:
                raise NotImplementedError("No URL defined for save on {}".format(self.__class__.__name__))
            resp = self._client.put(url, self.as_dict())
        self.update_from_dict(resp.json())


class Model(six.with_metaclass(MetaModel)):
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
        if kwarg_names:
            raise TypeError(
                "{}() got unexpected keyword-arguments: {}".format(self.__class__.__name__, ", ".join(kwarg_names)))
        if self._new:
            self._validate_fields()

    def _validate_fields(self):
        for field in self._meta.fields:
            if not field.is_valid(self):
                raise TypeError("Value of field {} is not valid on {}".format(field.name, self))

    def as_dict(self):
        if all(getattr(self, field.name) == field.default_value for field in self._meta.fields):
            return None
        d = {}
        for field in self._meta.fields:
            value = field.dump(self)
            if value is not None:
                d[_api_name(field.name)] = value
        return d

    def merge(self, other):
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
        return "{}({})".format(self.__class__.__name__,
                               ", ".join("{}={}".format(key, getattr(self, key)) for key in self._meta.field_names))

    def __eq__(self, other):
        try:
            return self.as_dict() == other.as_dict()
        except AttributeError:
            return False


def _api_name(name):
    return name[1:] if name.startswith("_") else name


class WatchEvent(object):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"

    def __init__(self, event_json, cls):
        self.type = event_json["type"]
        self.object = cls.from_dict(event_json["object"])

    def __repr__(self):
        return "{cls}(type={type}, object={object})".format(cls=self.__class__.__name__, type=self.type,
                                                            object=self.object)
