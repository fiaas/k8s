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

from k8s.client import NotFound
from k8s.models.common import ObjectMeta
from k8s.models.networking_v1_ingress import Ingress, IngressSpec, IngressRule, IngressBackend, HTTPIngressPath, \
    HTTPIngressRuleValue, IngressServiceBackend, ServiceBackendPort

NAME = "my-name"
NAMESPACE = "my-namespace"


# pylint: disable=R0201
@pytest.mark.usefixtures("k8s_config")
class TestIngress(object):
    def test_create_blank(self):
        object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
        ingress = Ingress(metadata=object_meta)
        assert ingress.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        ingress = _create_default_ingress()
        call_params = ingress.as_dict()
        post.return_value.json.return_value = call_params

        assert ingress._new
        ingress.save()
        assert not ingress._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        ingress = _create_default_ingress()

        from_api = Ingress.get_or_create(metadata=ingress.metadata, spec=ingress.spec)
        assert not from_api._new
        assert from_api.spec.rules[0].host == "dummy.example.com"
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "creationTimestamp": "2016-11-23T13:43:42Z",
            "generation": 7,
            "labels": {
                "test": "true"
            },
            "name": NAME,
            "namespace": NAMESPACE,
            "resourceVersion": "96758807",
            "selfLink": _uri(NAMESPACE, NAME),
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "spec": {
            'ingressClassName': 'my-class',
            'defaultBackend': {
                'service': {
                    'name': 'default-dummy',
                    'port': {
                        'name': 'http',
                    },
                },
            },
            'tls': [],
            'rules': [
                {
                    'host': 'old-dummy.example.com',
                    'http': {
                        'paths': [
                            {
                                'path': '/',
                                'backend': {
                                    'service': {
                                        'name': 'dummy',
                                        'port': {
                                            'name': 'http',
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        },
        "status": {
            "loadBalancer": {}
        }
    }
    return mock_response


def _create_default_ingress():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    ingress_backend = IngressBackend(IngressServiceBackend(name="dummy", port=ServiceBackendPort(name="http")))
    http_ingress_path = HTTPIngressPath(path="/", backend=ingress_backend)
    http_ingress_rule = HTTPIngressRuleValue(paths=[http_ingress_path])
    ingress_rule = IngressRule(host="dummy.example.com", http=http_ingress_rule)
    ingress_spec = IngressSpec(rules=[ingress_rule])
    ingress = Ingress(metadata=object_meta, spec=ingress_spec)
    return ingress


def _uri(namespace, name=""):
    return "/apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}".format(name=name, namespace=namespace)
