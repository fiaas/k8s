#!/usr/bin/env python
# -*- coding: utf-8

"""Singleton configuration for k8s client"""

#: API server URL
api_server = "https://kubernetes.default.svc.cluster.local"
#: API token
api_token = ""
#: API certificate
cert = None
#: Should the client verify the servers SSL certificates?
verify_ssl = True
#: Enable debugging
debug = False
#: Default timeout for most operations
timeout = 20
#: Default timeout for streaming operations
stream_timeout = 3600
#: Default size of Watcher cache
watcher_cache_size = 1000
