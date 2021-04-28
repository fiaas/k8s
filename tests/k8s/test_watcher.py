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


import mock
from mock import call
import pytest
import six

from k8s.base import Model, Field, WatchEvent
from k8s.models.common import ObjectMeta
from k8s.watcher import Watcher

# Just to make things shorter
ADDED = WatchEvent.ADDED
MODIFIED = WatchEvent.MODIFIED
DELETED = WatchEvent.DELETED
BOOKMARK = WatchEvent.BOOKMARK


@pytest.mark.usefixtures("k8s_config", "logger")
class TestWatcher(object):
    @pytest.fixture
    def api_watch_list(self):
        with mock.patch('k8s.base.ApiMixIn.watch_list') as m:
            yield m

    def test_multiple_events(self, api_watch_list):
        number_of_events = 20
        events = [_event(i, ADDED, 1) for i in range(number_of_events)]
        api_watch_list.side_effect = [events]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        for i in range(number_of_events):
            _assert_event(next(gen), i, ADDED, 1)
        watcher._run_forever = False
        assert list(gen) == []

        api_watch_list.assert_called_with(namespace=None, start_at_resource_version=None)

    def test_handle_reconnect(self, api_watch_list):
        events = [_event(0, ADDED, 1)]
        api_watch_list.side_effect = [events, events]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        watcher._run_forever = False
        assert list(gen) == []

    def test_handle_changes(self, api_watch_list):
        events = [_event(0, ADDED, 1), _event(0, MODIFIED, 2)]
        api_watch_list.side_effect = [events]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 0, MODIFIED, 2)

        watcher._run_forever = False
        assert list(gen) == []

    def test_many_reconnections(self, api_watch_list):
        first = [_event(0, ADDED, 1), _event(1, ADDED, 1), _event(2, ADDED, 1)]
        second = [_event(3, ADDED, 1), _event(4, ADDED, 2), _event(5, ADDED, 1), _event(6, MODIFIED, 2)]
        third = [_event(7, ADDED, 2), _event(8, DELETED, 2), _event(9, ADDED, 1), _event(20, BOOKMARK, 2)]
        fourth = [_event(25, ADDED, 2), _event(26, ADDED, 1), _event(27, MODIFIED, 2)]
        api_watch_list.side_effect = [first, second, third, fourth]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        # First batch
        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 1, ADDED, 1)
        _assert_event(next(gen), 2, ADDED, 1)

        # Second batch
        _assert_event(next(gen), 3, ADDED, 1)
        _assert_event(next(gen), 4, ADDED, 2)
        _assert_event(next(gen), 5, ADDED, 1)
        _assert_event(next(gen), 6, MODIFIED, 2)

        # Third batch
        _assert_event(next(gen), 7, ADDED, 2)
        _assert_event(next(gen), 8, DELETED, 2)
        _assert_event(next(gen), 9, ADDED, 1)

        # Fourth batch
        _assert_event(next(gen), 25, ADDED, 2)
        _assert_event(next(gen), 26, ADDED, 1)
        _assert_event(next(gen), 27, MODIFIED, 2)

        watcher._run_forever = False
        assert list(gen) == []

    def test_start_watching_from_bookmark(self, api_watch_list):

        bookmark_event = _event(30, BOOKMARK, 1)
        first = [_event(0, ADDED, 1), _event(1, ADDED, 1), _event(2, ADDED, 1), bookmark_event]
        second = [_event(31, ADDED, 1)]

        api_watch_list.side_effect = [first, second]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 1, ADDED, 1)
        _assert_event(next(gen), 2, ADDED, 1)
        _assert_event(next(gen), 31, ADDED, 1)

        api_watch_list.assert_has_calls([
            call(namespace=None, start_at_resource_version=None),
            call(namespace=None, start_at_resource_version=bookmark_event.resourceVersion),
        ])

    def test_namespace(self, api_watch_list):
        namespace = "the-namespace"
        watcher = Watcher(WatchListExample)

        def stop_iteration(*args, **kwargs):
            watcher._run_forever = False
            return []
        api_watch_list.side_effect = stop_iteration

        gen = watcher.watch(namespace=namespace)

        assert list(gen) == []

        api_watch_list.assert_called_with(namespace=namespace, start_at_resource_version=None)


def _event(id, event_type, rv):
    event_json = {
        "type": event_type,
        "object": {
            "value": (id * 100) + rv,
            "metadata": {
                "resourceVersion": rv
            }
        },
    }
    we = WatchEvent(event_json, WatchListExample)
    return mock.NonCallableMagicMock(type=event_type, object=we)


def _assert_event(event, id, event_type, rv):
    assert event.type == event_type
    o = event.object.object
    assert o.kind == "Example"
    assert o.value == (id * 100) + rv


class WatchListExample(Model):
    class Meta:
        url_template = '/example'
        watch_list_url = '/watch/example'
        watch_list_url_template = '/watch/{namespace}/example'

    apiVersion = Field(six.text_type, "example.com/v1")
    kind = Field(six.text_type, "Example")
    metadata = Field(ObjectMeta)
    value = Field(int)


class SentinelException(Exception):
    pass
