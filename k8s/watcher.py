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

from .base import WatchEvent

DEFAULT_CAPACITY = 1000


class Watcher(object):
    """Higher-level interface to watch for changes in objects

    The low-level :py:meth:`~.watch_list` method will stop when the API-server drops the connection.
    When reconnecting, the API-server lets the caller specify which watch event to restart from.

    The Watcher will hide this complexity for you, and make sure to reconnect when the
    connection drops, and restart the watch from the last observed event. 

    :param Model model: The model class to watch
    """
    def __init__(self, model):
        self._model = model
        self._run_forever = True

    def watch(self, namespace=None, start_at_resource_version=None):
        """Watch for events

        :param str namespace: the namespace to watch for events in. The default (None) results in
            watching for events in all namespaces.
        :param int start_at_resource_version: the resource version to begin watching at, excluding 
            the version number itself. The default (None) will send the most recent event, then 
            begin watching events occuring thereafter.
        :return: a generator that yields :py:class:`~.WatchEvent` objects not seen before
        """

        last_seen_version = start_at_resource_version

        while self._run_forever:
            for event in self._model.watch_list(
                namespace=namespace, 
                start_at_resource_version=last_seen_version
            ):
                last_seen_version = event.resourceVersion
                if event.type != WatchEvent.BOOKMARK:
                    yield event
