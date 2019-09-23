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

from .base import WatchEvent

DEFAULT_CAPACITY = 1000


class Watcher(object):
    """Higher-level interface to watch for changes in objects

    The low-level :py:meth:`~.watch_list` method will stop when the API-server drops the connection.
    When reconnecting, the API-server will send a list of :py:const:`~k8s.base.WatchEvent.ADDED`
    events for all objects, even if they have been seen before.

    The Watcher will hide this complexity for you, and make sure to reconnect when the
    connection drops, and skip events that have already been seen.

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
        while self._run_forever:
            for event in self._model.watch_list(namespace=namespace):
                o = event.object
                key = (o.metadata.name, o.metadata.namespace)
                if self._seen.get(key) == o.metadata.resourceVersion and event.type != WatchEvent.DELETED:
                    continue
                self._seen[key] = o.metadata.resourceVersion
                yield event
