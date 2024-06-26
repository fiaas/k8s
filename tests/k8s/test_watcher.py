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
import pytest

from k8s.base import APIServerError, Field, Model, WatchBookmark, WatchEvent, ModelList, ListMeta
from k8s.models.common import ObjectMeta
from k8s.watcher import Watcher

# Just to make things shorter
ADDED = WatchEvent.ADDED
MODIFIED = WatchEvent.MODIFIED
DELETED = WatchEvent.DELETED


class WatchListExample(Model):
    class Meta:
        url_template = '/example'
        watch_list_url = '/watch/example'
        watch_list_url_template = '/watch/{namespace}/example'

    apiVersion = Field(str, "example.com/v1")
    kind = Field(str, "Example")
    metadata = Field(ObjectMeta)
    value = Field(int)


def _example_resource(_id, rv, namespace="default"):
    metadict = {"name": "name{}".format(_id), "namespace": namespace, "resourceVersion": str(rv)}
    metadata = ObjectMeta.from_dict(metadict)
    return WatchListExample(metadata=metadata, value=(_id * 100) + rv)


def _event(_id, event_type, rv, namespace="default"):
    wle = _example_resource(_id, rv, namespace)
    return WatchEvent(_type=event_type, _object=wle)


def _assert_event(event, _id, event_type, rv, namespace="default"):
    assert event.type == event_type
    o = event.object
    assert o.kind == "Example"
    assert o.metadata.name == "name{}".format(_id)
    assert o.metadata.namespace == namespace
    assert o.value == (_id * 100) + rv


@pytest.mark.usefixtures("k8s_config", "logger")
class TestWatcher(object):
    @pytest.fixture
    def api_list_with_meta(self):
        with mock.patch("k8s.base.ApiMixIn.list_with_meta") as m:
            yield m

    @pytest.fixture
    def api_watch_list(self):
        with mock.patch("k8s.base.ApiMixIn.watch_list") as m:
            yield m

    @pytest.mark.parametrize(
        'initial_resources,list_resource_version,events',
        (
            # 20 initial resources, then 20 watch events
            ([_example_resource(i, 100 + i) for i in range(20)], "200", [_event(i, ADDED, 300 + i) for i in range(20)]),
            # 20 initial resources, no watch events
            ([_example_resource(i, 100 + i) for i in range(20)], "200", []),
            # no initial resources, 20  watch events
            ([], "1", [_event(i, ADDED, 300 + i) for i in range(20)]),
        ),
    )
    def test_multiple_events(
        self, api_watch_list, api_list_with_meta, initial_resources, list_resource_version, events
    ):
        model_list = ModelList(metadata=ListMeta(resourceVersion=list_resource_version), items=initial_resources)
        api_list_with_meta.return_value = model_list
        api_watch_list.side_effect = [events]

        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        # verify that the initial resources are yielded by the watcher first
        for i in range(len(initial_resources)):
            _assert_event(next(gen), i, ADDED, 100 + i)

        # verify that the events from the watch_list call are yielded by the watcher
        for i in range(len(events)):
            _assert_event(next(gen), i, ADDED, 300 + i)

        # stop the watcher loop and verify that there are no more events
        watcher._run_forever = False
        assert list(gen) == []

        api_list_with_meta.assert_called_with(namespace=None)
        # verify watch_list was called with resourceVersion returned by list call
        api_watch_list.assert_called_with(namespace=None, resource_version=list_resource_version, allow_bookmarks=True)

    def test_no_events(self, api_watch_list, api_list_with_meta):
        list_resource_version = "1"
        model_list = ModelList(metadata=ListMeta(resourceVersion=list_resource_version), items=[])
        api_list_with_meta.return_value = model_list

        def stop_iteration(*args, **kwargs):
            watcher._run_forever = False
            return []

        api_watch_list.side_effect = stop_iteration

        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        assert list(gen) == []

        api_list_with_meta.assert_called_with(namespace=None)
        # verify watch_list was called with resourceVersion returned by list call
        api_watch_list.assert_called_with(namespace=None, resource_version=list_resource_version, allow_bookmarks=True)

    def test_handle_watcher_cache_watch(self, api_watch_list, api_list_with_meta):
        # if the same event (same name, namespace and resource version) is returned by watch_list multiple times, it
        # should only be yielded once. If a DELETED event is received with the same resourceVersion, it should be
        # yielded.
        # If a DELETED event is received with the same resourceVersion as a previous event, it should be yielded.
        model_list = ModelList(metadata=ListMeta(resourceVersion="1"), items=[])
        api_list_with_meta.return_value = model_list

        # yield event with resource twice, and stop the watcher after yielding the second event
        event = _event(0, ADDED, 1)
        delete_event = _event(0, DELETED, 1)

        def side_effect(*args, **kwargs):
            yield event
            yield event
            yield delete_event
            watcher._run_forever = False

        api_watch_list.side_effect = side_effect

        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 0, DELETED, 1)
        assert list(gen) == []

    def test_handle_watcher_cache_list(self, api_watch_list, api_list_with_meta):
        # if the same event (same name, namespace and resource version) is returned by list and watch_list multiple
        # times, it should only be yielded once.
        # If a DELETED event is received with the same resourceVersion as a previous event, it should be yielded.
        resource = _example_resource(0, 1)
        model_list = ModelList(metadata=ListMeta(resourceVersion="1"), items=[resource])
        api_list_with_meta.return_value = model_list

        # yield event twice, and stop the watcher after yielding the second event
        event = WatchEvent(_type=WatchEvent.ADDED, _object=resource)
        delete_event = WatchEvent(_type=WatchEvent.DELETED, _object=resource)

        def side_effect(*args, **kwargs):
            yield event
            yield event
            yield delete_event
            watcher._run_forever = False

        api_watch_list.side_effect = side_effect

        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 0, DELETED, 1)
        assert list(gen) == []

    def test_handle_changes(self, api_watch_list, api_list_with_meta):
        model_list = ModelList(metadata=ListMeta(resourceVersion="1"), items=[])
        api_list_with_meta.return_value = model_list

        events = [_event(0, ADDED, 1), _event(0, MODIFIED, 2)]
        api_watch_list.side_effect = [events]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 0, MODIFIED, 2)

        watcher._run_forever = False
        assert list(gen) == []

    def test_complicated(self, api_watch_list, api_list_with_meta):
        initial_resources = [_example_resource(1, 0), _example_resource(2, 0)]
        model_list = ModelList(metadata=ListMeta(resourceVersion="1"), items=initial_resources)
        api_list_with_meta.return_value = model_list

        first = [_event(0, ADDED, 1), _event(1, ADDED, 1), _event(2, ADDED, 1)]
        second = [_event(0, ADDED, 1), _event(1, ADDED, 2), _event(2, ADDED, 1), _event(0, MODIFIED, 2)]
        third = [_event(0, ADDED, 2), _event(1, DELETED, 2), _event(2, ADDED, 1), _event(2, MODIFIED, 2)]
        fourth = [_event(0, ADDED, 2), _event(0, ADDED, 1, "other"), _event(0, MODIFIED, 2, "other")]
        api_watch_list.side_effect = [first, second, third, fourth]
        watcher = Watcher(WatchListExample)
        gen = watcher.watch()

        # Synthetic added events for the initial resources
        _assert_event(next(gen), 1, ADDED, 0)
        _assert_event(next(gen), 2, ADDED, 0)

        # First batch of events
        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 1, ADDED, 1)
        _assert_event(next(gen), 2, ADDED, 1)

        # Second batch of events
        _assert_event(next(gen), 1, ADDED, 2)
        _assert_event(next(gen), 0, MODIFIED, 2)

        # Third batch of events
        _assert_event(next(gen), 1, DELETED, 2)
        _assert_event(next(gen), 2, MODIFIED, 2)

        # Fourth batch of events
        _assert_event(next(gen), 0, ADDED, 1, "other")
        _assert_event(next(gen), 0, MODIFIED, 2, "other")

        watcher._run_forever = False
        assert list(gen) == []

    def test_namespace(self, api_watch_list, api_list_with_meta):
        namespace = "the-namespace"
        watcher = Watcher(WatchListExample)

        api_list_with_meta.return_value = ModelList(metadata=ListMeta(), items=[])

        def stop_iteration(*args, **kwargs):
            watcher._run_forever = False
            return []

        api_watch_list.side_effect = stop_iteration

        gen = watcher.watch(namespace=namespace)

        assert list(gen) == []

        api_list_with_meta.assert_called_with(namespace=namespace)
        api_watch_list.assert_called_with(namespace=namespace, resource_version=None, allow_bookmarks=True)

    def test_handle_410_list(self, api_watch_list, api_list_with_meta):
        # the initial list call should not receive 410, since it doesn't send a resourceversion. If it does, something
        # is probably wrong, and the exception should be propagated to the caller.
        api_list_with_meta.side_effect = APIServerError({"code": 410, "message": "Gone"})

        watcher = Watcher(WatchListExample)
        with pytest.raises(APIServerError, match="Gone"):
            next(watcher.watch())

    def test_handle_410_watch(self, api_watch_list, api_list_with_meta):
        # 410 response can occur if watch connection starts with a too old resourceVersion
        # - this can happen on reconnect if last_seen_resource_version is too old, for example if the apiserver
        #   doesn't send bookmark events, or sends them at intervals longer than the client watch timeout
        #   (k8s.config.stream_timeout, default 4.5 minutes)
        # - in theory the resourceVersion returned by the list call could be too old when the watch connection starts
        #   if it takes too long to yield syntetic added watch events for the items returned by the list call.
        #   How long this takes depends on the consumer of the generator returned by watcher.watch(). If this happens,
        #   the watcher will do another quorum read. Since there is a cache of seen items in the watcher, as long as
        #   all items fit in the cache, the number of events yielded for items from the list call approach zero,
        #   eventually allowing the watch connection to start.
        watcher = Watcher(WatchListExample)

        first_list_resource_version = "1"
        second_list_resource_version = "4"
        api_list_with_meta.side_effect = [
            ModelList(metadata=ListMeta(resourceVersion=first_list_resource_version), items=[_example_resource(0, 0)]),
            ModelList(metadata=ListMeta(resourceVersion=second_list_resource_version), items=[_example_resource(0, 0)]),
        ]

        api_watch_list.return_value.__getitem__.side_effect = [
            _event(1, ADDED, 2),
            APIServerError({"code": 410, "message": "Gone"}),
            _event(1, MODIFIED, 3),
        ]
        # Seal the mock to make sure __iter__ is not used instead of __getitem__
        mock.seal(api_watch_list)

        gen = watcher.watch()

        # synthetic added event for initial resource and added event
        _assert_event(next(gen), 0, ADDED, 0)
        _assert_event(next(gen), 1, ADDED, 2)
        api_list_with_meta.assert_called_once()
        api_watch_list.assert_called_once_with(
            namespace=None, resource_version=first_list_resource_version, allow_bookmarks=True
        )

        # next will raise 410 from watch_list, call list and watch_list again, then yield the last event
        _assert_event(next(gen), 1, MODIFIED, 3)
        # verify list and watch_list has now been called twice, and each call of watch_list used the resourceVersion
        # returned by the preceding list call
        assert api_list_with_meta.call_args_list == [mock.call(namespace=None), mock.call(namespace=None)]
        assert api_watch_list.call_args_list == [
            mock.call(namespace=None, resource_version=first_list_resource_version, allow_bookmarks=True),
            mock.call(namespace=None, resource_version=second_list_resource_version, allow_bookmarks=True),
        ]

        # no more events
        watcher._run_forever = False
        assert list(gen) == []

    def test_other_apierror_list(self, api_list_with_meta):
        watcher = Watcher(WatchListExample)

        api_list_with_meta.side_effect = APIServerError({"code": 400, "message": "Bad Request"})

        with pytest.raises(APIServerError, match="Bad Request"):
            next(watcher.watch())

    def test_other_apierror_watch(self, api_watch_list, api_list_with_meta):
        watcher = Watcher(WatchListExample)

        api_list_with_meta.return_value = ModelList(metadata=ListMeta(), items=[])
        api_watch_list.side_effect = APIServerError({"code": 400, "message": "Bad Request"})
        with pytest.raises(APIServerError, match="Bad Request"):
            next(watcher.watch())

    def test_bookmark(self, api_watch_list, api_list_with_meta):
        watcher = Watcher(WatchListExample)
        api_list_with_meta.return_value = ModelList(metadata=ListMeta(), items=[])

        watcher = Watcher(WatchListExample)

        api_watch_list.return_value.__getitem__.side_effect = [
            _event(0, ADDED, 1),
            WatchBookmark({"object": {"metadata": {"resourceVersion": "2"}}}),
            _event(1, MODIFIED, 3),
        ]
        # Seal the mock to make sure __iter__ is not used instead of __getitem__
        mock.seal(api_watch_list)

        gen = watcher.watch()
        _assert_event(next(gen), 0, ADDED, 1)
        _assert_event(next(gen), 1, MODIFIED, 3)
        watcher._run_forever = False
        assert list(gen) == []
