#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest
import six

from k8s.base import Model, Field, WatchEvent
from k8s.models.common import ObjectMeta
from k8s.watcher import Watcher

# Just to make things shorter
ADDED = WatchEvent.ADDED
MODIFIED = WatchEvent.MODIFIED
DELETED = WatchEvent.DELETED


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
        gen = Watcher(WatchListExample).watch()

        for i in range(number_of_events):
            _assert_event(next(gen), i, ADDED, 1)
        with pytest.raises(StopIteration):
            next(gen)

        api_watch_list.assert_called_with(namespace=None)

    def test_handle_reconnect(self, api_watch_list):
        events = [_event(0, ADDED, 1)]
        api_watch_list.side_effect = [events, events]
        gen = Watcher(WatchListExample).watch()

        _assert_event(next(gen), 0, ADDED, 1)
        with pytest.raises(StopIteration):
            next(gen)

    def test_handle_changes(self, api_watch_list):
        events = [_event(0, ADDED, 1), _event(0, MODIFIED, 2)]
        api_watch_list.side_effect = [events]
        gen = Watcher(WatchListExample).watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 0, MODIFIED, 2)

        with pytest.raises(StopIteration):
            next(gen)

    def test_complicated(self, api_watch_list):
        first = [_event(0, ADDED, 1), _event(1, ADDED, 1), _event(2, ADDED, 1)]
        second = [_event(0, ADDED, 1), _event(1, ADDED, 2), _event(2, ADDED, 1), _event(0, MODIFIED, 2)]
        third = [_event(0, ADDED, 2), _event(1, DELETED, 2), _event(2, ADDED, 1), _event(2, MODIFIED, 2)]
        fourth = [_event(0, ADDED, 2), _event(0, ADDED, 1, "other"), _event(0, MODIFIED, 2, "other")]
        api_watch_list.side_effect = [first, second, third, fourth]
        gen = Watcher(WatchListExample).watch()

        # First batch
        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 1, ADDED, 1)
        _assert_event(next(gen), 2, ADDED, 1)

        # Second batch
        _assert_event(next(gen), 1, ADDED, 2)
        _assert_event(next(gen), 0, MODIFIED, 2)

        # Third batch
        _assert_event(next(gen), 1, DELETED, 2)
        _assert_event(next(gen), 2, MODIFIED, 2)

        # Fourth batch
        _assert_event(next(gen), 0, ADDED, 1, "other")
        _assert_event(next(gen), 0, MODIFIED, 2, "other")

        with pytest.raises(StopIteration):
            next(gen)

    def test_namespace(self, api_watch_list):
        namespace = "the-namespace"
        api_watch_list.side_effect = []

        gen = Watcher(WatchListExample).watch(namespace=namespace)

        with pytest.raises(StopIteration):
            next(gen)

        api_watch_list.assert_called_with(namespace=namespace)


def _event(id, event_type, rv, namespace="default"):
    metadict = {"name": "name{}".format(id), "namespace": namespace, "resourceVersion": rv}
    metadata = ObjectMeta.from_dict(metadict)
    wle = WatchListExample(metadata=metadata, value=(id * 100) + rv)
    return mock.NonCallableMagicMock(type=event_type, object=wle)


def _assert_event(event, id, event_type, rv, namespace="default"):
    assert event.type == event_type
    o = event.object
    assert o.kind == "Example"
    assert o.metadata.name == "name{}".format(id)
    assert o.metadata.namespace == namespace
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
