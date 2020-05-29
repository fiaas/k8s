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

from k8s.base import Model, Field, WatchEvent, Equality, Inequality, In, NotIn, Exists
from k8s.models.common import DeleteOptions, Preconditions


class Example(Model):
    class Meta:
        url_template = '/example'
        watch_list_url = '/watch/example'

    value = Field(int)


class TestWatchEvent(object):
    def test_watch_event_added(self):
        watch_event = WatchEvent({"type": "ADDED", "object": {"value": 42}}, Example)
        assert watch_event.type == WatchEvent.ADDED
        assert watch_event.object == Example(value=42)

    def test_watch_event_modified(self):
        watch_event = WatchEvent({"type": "MODIFIED", "object": {"value": 42}}, Example)
        assert watch_event.type == WatchEvent.MODIFIED
        assert watch_event.object == Example(value=42)

    def test_watch_event_deleted(self):
        watch_event = WatchEvent({"type": "DELETED", "object": {"value": 42}}, Example)
        assert watch_event.type == WatchEvent.DELETED
        assert watch_event.object == Example(value=42)


class TestFind(object):
    @pytest.fixture
    def client(self):
        with mock.patch.object(Example, "_client") as m:
            yield m

    def test_find_by_name(self, client):
        Example.find("app_name")
        client.get.assert_called_once_with("/example", params={"labelSelector": "app=app_name"})

    @pytest.mark.parametrize("value, selector", (
        (Equality("my_value"), "my_key=my_value"),
        (Inequality("my_value"), "my_key!=my_value"),
        (In(("value1", "value2")), "my_key in (value1,value2)"),
        (NotIn(("value1", "value2")), "my_key notin (value1,value2)"),
        (Exists(), "my_key"),
        ("my_unwrapped_value", "my_key=my_unwrapped_value"),
    ))
    def test_find_by_selectors(self, client, value, selector):
        Example.find(labels={"my_key": value})
        client.get.assert_called_once_with("/example", params={"labelSelector": selector})

    def test_repeated_keys_in_label_selector(self, client):
        labels = [
            ("foo", Inequality("bar")),
            ("foo", Exists())
        ]
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
            propagationPolicy="Foreground"
        )
        Example.delete_list(labels={"foo": "bar"}, delete_options=opts)

        expected_body = {
            "apiVersion": "foo/v1",
            "dryRun": [],
            "gracePeriodSeconds": 30,
            "preconditions": {
                "uid": "1234",
                "resourceVersion": "12"
            },
            "propagationPolicy": "Foreground"
        }
        client.delete.assert_called_once_with("/example", params={"labelSelector": "foo=bar"}, body=expected_body)