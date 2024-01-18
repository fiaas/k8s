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


import cachetools

from .base import APIServerError, WatchEvent

DEFAULT_CAPACITY = 1000


class Watcher(object):
    """Higher-level interface to watch for changes in objects

    The low-level :py:meth:`~.watch_list` method will stop when the API-server drops the connection.
    When reconnecting using that method, the API-server will send a list of :py:const:`~k8s.base.WatchEvent.ADDED`
    events for all objects, even if they have been seen before.

    The Watcher will hide this complexity for you, and make sure to reconnect when the
    connection drops, and skip events that have already been seen.
    It additionally uses bookmarks to avoid the increased load that might be caused by reconnecting.

    :param Model model: The model class to watch
    :param int capacity: How many seen objects to keep track of
    """

    def __init__(self, model, capacity=DEFAULT_CAPACITY):
        self._seen = cachetools.LRUCache(capacity)
        self._model = model
        self._run_forever = True

    def watch(self, namespace=None):
        """Watch for events

        :param str namespace: the namespace to watch for events in. The default (None) results in
            watching for events in all namespaces.
        :return: a generator that yields :py:class:`~.WatchEvent` objects not seen before
        """
        # last_seen_resource_version is used to resume the watch from the last seen event.
        # Only used on reconnects, the first call to watch does a quorum read.
        last_seen_resource_version = None
        while self._run_forever:
            try:
                for event in self._model.watch_list(
                    namespace=namespace, resource_version=last_seen_resource_version, allow_bookmarks=True
                ):
                    last_seen_resource_version = event.resource_version
                    if self._should_yield(event):
                        yield event
            except APIServerError as e:
                # A 410 response indicates our resourceVersion is too old, and we need to do a new quorum read.
                if e.api_error["code"] == 410:
                    last_seen_resource_version = None
                else:
                    raise

    def _should_yield(self, event) -> bool:
        """Check if this is a new event, and if so, mark it as seen"""
        if not event.has_object():
            return False
        o = event.object
        key = (o.metadata.name, o.metadata.namespace)
        if self._seen.get(key) == o.metadata.resourceVersion and event.type != WatchEvent.DELETED:
            return False
        self._seen[key] = o.metadata.resourceVersion
        return True
