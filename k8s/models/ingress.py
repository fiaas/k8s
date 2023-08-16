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


from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class IngressBackend(Model):
    serviceName = Field(str)
    servicePort = Field(str)


class HTTPIngressPath(Model):
    path = Field(str)
    backend = Field(IngressBackend)


class HTTPIngressRuleValue(Model):
    paths = ListField(HTTPIngressPath)


class IngressRule(Model):
    host = Field(str)
    http = Field(HTTPIngressRuleValue)


class IngressTLS(Model):
    hosts = ListField(str)
    secretName = Field(str)


class IngressSpec(Model):
    backend = Field(IngressBackend)
    rules = ListField(IngressRule)
    tls = ListField(IngressTLS)


class Ingress(Model):
    class Meta:
        list_url = "/apis/extensions/v1beta1/ingresses"
        url_template = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}"
        watch_list_url = "/apis/extensions/v1beta1/watch/ingresses"

    metadata = Field(ObjectMeta)
    spec = Field(IngressSpec)
