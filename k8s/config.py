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
