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


from .common import ObjectMeta, TypedLocalObjectReference
from ..base import Model
from ..fields import Field, ListField


class ServiceBackendPort(Model):
    name = Field(str)
    number = Field(int)


class IngressServiceBackend(Model):
    name = Field(str)
    port = Field(ServiceBackendPort)


class IngressBackend(Model):
    resource = Field(TypedLocalObjectReference)
    service = Field(IngressServiceBackend)


class HTTPIngressPath(Model):
    backend = Field(IngressBackend)
    path = Field(str)
    pathType = Field(str)


class HTTPIngressRuleValue(Model):
    paths = ListField(HTTPIngressPath)


class IngressRule(Model):
    host = Field(str)
    http = Field(HTTPIngressRuleValue)


class IngressTLS(Model):
    hosts = ListField(str)
    secretName = Field(str)


class IngressSpec(Model):
    defaultBackend = Field(IngressBackend)
    ingressClassName = Field(str)
    rules = ListField(IngressRule)
    tls = ListField(IngressTLS)


class PortStatus(Model):
    error = Field(str)
    port = Field(int)
    protocol = Field(str)


class LoadBalancerIngress(Model):
    hostname = Field(str)
    ip = Field(str)
    ports = ListField(PortStatus)


class LoadBalancerStatus(Model):
    ingress = ListField(LoadBalancerIngress)


class IngressStatus(Model):
    loadBalancer = Field(LoadBalancerStatus)


class Ingress(Model):
    class Meta:
        list_url = "/apis/networking.k8s.io/v1/ingresses"
        url_template = "/apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}"
        watch_list_url = "/apis/networking.k8s.io/v1/ingresses?watch=true"

    metadata = Field(ObjectMeta)
    spec = Field(IngressSpec)
    status = Field(IngressStatus)
