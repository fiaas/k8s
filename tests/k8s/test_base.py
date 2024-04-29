#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import mock
import pytest
import requests
import requests.packages.urllib3 as urllib3

from k8s.base import APIServerError, Equality, Exists, Field, In, Inequality, Model, NotIn, WatchBookmark, WatchEvent
from k8s.client import NotFound, ServerError, ClientError
from k8s.models.common import DeleteOptions, Preconditions, ObjectMeta


class Example(Model):
    class Meta:
        url_template = '/example'
        watch_list_url = '/watch/example'

    metadata = Field(ObjectMeta)
    value = Field(int)


def _example_object(value=42, resource_version="1"):
    # Since metadata.resourceVersion is a ReadOnlyField values set are ignored. To avoid this we have to use from_dict
    # to set the field value, like when deserializing an API response.
    metadata = ObjectMeta.from_dict({"resourceVersion": resource_version})
    return Example(metadata=metadata, value=value)


class TestWatchEvent(object):
    def test_watch_event_added(self):
        obj = _example_object(42, "1")
        event_dict = {"type": "ADDED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}}
        watch_event = WatchEvent(event_dict, Example)
        assert watch_event.type == WatchEvent.ADDED
        assert watch_event.object == obj

    def test_watch_event_modified(self):
        obj = _example_object(42, "1")
        event_dict = {"type": "MODIFIED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}}
        watch_event = WatchEvent(event_dict, Example)
        assert watch_event.type == WatchEvent.MODIFIED
        assert watch_event.object == obj

    def test_watch_event_deleted(self):
        obj = _example_object(42, "1")
        event_dict = {"type": "DELETED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}}
        watch_event = WatchEvent(event_dict, Example)
        assert watch_event.type == WatchEvent.DELETED
        assert watch_event.object == obj

    @pytest.mark.parametrize(
        "_type",
        (
            WatchEvent.ADDED,
            WatchEvent.MODIFIED,
            WatchEvent.DELETED,
        ),
    )
    def test_watch_event_type_object(self, _type):
        obj = _example_object(42, "1")
        watch_event = WatchEvent(_type=_type, _object=obj)
        assert watch_event.type == _type
        assert watch_event.object == obj

    @pytest.mark.parametrize(
        "kwargs",
        (
            # invalid combinations of keyword arguments
            dict(
                event_json={"type": "MODIFIED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}},
                _type=WatchEvent.MODIFIED,
            ),
            dict(
                event_json={"type": "MODIFIED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}},
                _object=_example_object(42, "1"),
            ),
            dict(cls=Example, _type=WatchEvent.MODIFIED),
            dict(cls=Example, _object=_example_object(42, "1")),
            # passed only one keyword argument, but a correct pair of arguments is required
            dict(event_json={"type": "MODIFIED", "object": {"metadata": {"resourceVersion": "1"}, "value": 42}}),
            dict(_object=_example_object(42, "1")),
            dict(_type=WatchEvent.MODIFIED),
            dict(cls=Example),
        ),
    )
    def test_watch_event_invalid_params(self, kwargs):
        with pytest.raises(ValueError):
            WatchEvent(**kwargs)


class TestFind(object):
    @pytest.fixture
    def client(self):
        with mock.patch.object(Example, "_client") as m:
            yield m

    def test_find_by_name(self, client):
        Example.find("app_name")
        client.get.assert_called_once_with("/example", params={"labelSelector": "app=app_name"})

    @pytest.mark.parametrize(
        "value, selector",
        (
            (Equality("my_value"), "my_key=my_value"),
            (Inequality("my_value"), "my_key!=my_value"),
            (In(("value1", "value2")), "my_key in (value1,value2)"),
            (NotIn(("value1", "value2")), "my_key notin (value1,value2)"),
            (Exists(), "my_key"),
            ("my_unwrapped_value", "my_key=my_unwrapped_value"),
        ),
    )
    def test_find_by_selectors(self, client, value, selector):
        Example.find(labels={"my_key": value})
        client.get.assert_called_once_with("/example", params={"labelSelector": selector})

    def test_repeated_keys_in_label_selector(self, client):
        labels = [("foo", Inequality("bar")), ("foo", Exists())]
        Example.find(labels=labels)

        expected_selector = "foo!=bar,foo"

        client.get.assert_called_once_with("/example", params={"labelSelector": expected_selector})


class TestDeleteList(object):
    @pytest.fixture
    def client(self):
        with mock.patch.object(Example, "_client") as m:
            yield m

    def test_delete_list(self, client):
        Example.delete_list(labels={"foo": Equality("bar"), "cat": Inequality("dog")})

        client.delete.assert_called_once_with("/example", body=None, params={"labelSelector": "cat!=dog,foo=bar"})

    def test_delete_with_options(self, client):
        opts = DeleteOptions(
            apiVersion="foo/v1",
            dryRun=[],
            gracePeriodSeconds=30,
            preconditions=Preconditions(uid="1234", resourceVersion="12"),
            propagationPolicy="Foreground",
        )
        Example.delete_list(labels={"foo": "bar"}, delete_options=opts)

        expected_body = {
            "apiVersion": "foo/v1",
            "dryRun": [],
            "gracePeriodSeconds": 30,
            "preconditions": {"uid": "1234", "resourceVersion": "12"},
            "propagationPolicy": "Foreground",
        }
        client.delete.assert_called_once_with("/example", params={"labelSelector": "foo=bar"}, body=expected_body)


class TestWatchList(object):
    @pytest.fixture
    def client(self):
        with mock.patch.object(Example, "_client") as m:
            yield m

    def test_watch_list(self, client):
        client.get.return_value.iter_lines.return_value = [
            '{"type": "ADDED", "object": {"metadata": {"resourceVersion": "1"}, "value": 1}}',
        ]
        gen = Example.watch_list()
        event_dict = {"type": "ADDED", "object": {"metadata": {"resourceVersion": "1"}, "value": 1}}
        assert next(gen) == WatchEvent(event_dict, Example)
        client.get.assert_called_once_with("/watch/example", stream=True, timeout=270, params={})
        assert list(gen) == []

    def test_watch_list_with_timeout(self, client):
        client.get.return_value.iter_lines.return_value.__getitem__.side_effect = [
            '{"type": "ADDED", "object": {"metadata": {"resourceVersion": "1"}, "value": 1}}',
            requests.ConnectionError(urllib3.exceptions.ReadTimeoutError("", "", "")),
            '{"type": "MODIFIED", "object": {"metadata": {"resourceVersion": "2"}, "value": 2}}',  # Not reached
        ]
        # Seal to avoid __iter__ being used instead of __getitem__
        mock.seal(client)
        gen = Example.watch_list()
        event_dict = {"type": "ADDED", "object": {"metadata": {"resourceVersion": "1"}, "value": 1}}
        assert next(gen) == WatchEvent(event_dict, Example)
        assert list(gen) == []
        assert client.get.return_value.iter_lines.return_value.__getitem__.call_count == 2
        client.get.assert_called_once_with("/watch/example", stream=True, timeout=270, params={})

    def test_watch_list_api_error(self, client):
        client.get.return_value.iter_lines.return_value = [
            '{"type": "ERROR", "object": {"kind":"Status", "code": 500, "message": "Internal Server Error"}}',
        ]
        gen = Example.watch_list()
        with pytest.raises(APIServerError, match="Internal Server Error"):
            next(gen)

    def test_watch_list_bookmark(self, client):
        client.get.return_value.iter_lines.return_value = [
            '{"type":"BOOKMARK", "object":{"metadata":{"resourceVersion": 4712}}}',
        ]
        gen = Example.watch_list(resource_version=4711, allow_bookmarks=True)
        assert next(gen) == WatchBookmark({"type": "BOOKMARK", "object": {"metadata": {"resourceVersion": 4712}}})
        assert list(gen) == []
        client.get.assert_called_once_with(
            "/watch/example", stream=True, timeout=270, params={"resourceVersion": 4711, "allowWatchBookmarks": "true"}
        )


class TestList:
    @pytest.fixture
    def response(self):
        data = {
            "metadata": {
                "resourceVersion": "1",
                "continue": "ENCODED_CONTINUE_TOKEN",
                "remainingItemCount": 1,
            },
            "items": [
                {"value": 42},
                {"value": 1337},
            ],
        }
        resp = mock.create_autospec(requests.Response, spec_set=True)
        resp.json.return_value = data
        yield resp

    @pytest.fixture
    def response_empty(self):
        data = {
            "metadata": {
                "resourceVersion": "2",
            },
            "items": [],
        }
        resp = mock.create_autospec(requests.Response, spec_set=True)
        resp.json.return_value = data
        yield resp

    @pytest.fixture
    def client(self):
        with mock.patch.object(Example, "_client") as m:
            yield m

    def test_list(self, client, response):
        client.get.return_value = response

        expected = [
            Example(value=42),
            Example(value=1337),
        ]
        assert Example.list() == expected

    def test_list_with_meta(self, client, response):
        client.get.return_value = response

        expected_items = [
            Example(value=42),
            Example(value=1337),
        ]

        actual = Example.list_with_meta()

        assert actual.metadata.resourceVersion == "1"
        assert actual.metadata._continue == "ENCODED_CONTINUE_TOKEN"
        assert actual.metadata.remainingItemCount == 1
        assert actual.items == expected_items

    def test_list_empty(self, client, response_empty):
        client.get.return_value = response_empty

        assert Example.list() == []

    def test_list_with_meta_empty(self, client, response_empty):
        client.get.return_value = response_empty

        actual = Example.list_with_meta()

        assert actual.metadata.resourceVersion == "2"
        assert actual.metadata._continue is None
        assert actual.metadata.remainingItemCount is None
        assert actual.items == []

    @pytest.mark.parametrize(
        "exception",
        (
            NotFound,
            ClientError,
            ServerError,
        ),
    )
    def test_list_error(self, client, exception):
        client.get.side_effect = exception

        with pytest.raises(exception):
            Example.list()

    @pytest.mark.parametrize(
        "exception",
        (
            NotFound,
            ClientError,
            ServerError,
        ),
    )
    def test_list_with_meta_error(self, client, exception):
        client.get.side_effect = exception

        with pytest.raises(exception):
            Example.list_with_meta()
