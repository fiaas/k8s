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

from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, OnceField, ListField


class ServicePort(Model):
    name = Field(six.text_type)
    protocol = Field(six.text_type, "TCP")
    port = Field(int)
    targetPort = Field(six.text_type)
    nodePort = Field(int)


class ServiceSpec(Model):
    ports = ListField(ServicePort)
    selector = Field(dict)
    clusterIP = OnceField(six.text_type)
    loadBalancerIP = OnceField(six.text_type)
    type = Field(six.text_type, "ClusterIP")
    sessionAffinity = Field(six.text_type, "None")
    loadBalancerSourceRanges = ListField(six.text_type)


class Service(Model):
    class Meta:
        list_url = "/api/v1/services"
        url_template = "/api/v1/namespaces/{namespace}/services/{name}"
        watch_list_url = "/api/v1/watch/services"

    metadata = Field(ObjectMeta)
    spec = Field(ServiceSpec)
