#!/usr/bin/env python
# -*- coding: utf-8

import cachetools

from k8s.base import WatchEvent

DEFAULT_CAPACITY = 1000


class Watcher(object):
    def __init__(self, model, capacity=DEFAULT_CAPACITY):
        self._seen = cachetools.LRUCache(capacity)
        self._model = model

    def watch(self):
        while True:
            for event in self._model.watch_list():
                o = event.object
                key = (o.metadata.name, o.metadata.namespace)
                if self._seen.get(key) == o.metadata.resourceVersion and event.type != WatchEvent.DELETED:
                    continue
                self._seen[key] = o.metadata.resourceVersion
                yield event
