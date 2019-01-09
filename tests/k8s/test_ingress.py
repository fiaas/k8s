#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta
from k8s.models.v1_6.kubernetes.apis.extensions.v1beta1 import Ingress, IngressBackend, HTTPIngressPath, \
    HTTPIngressRuleValue, IngressRule, IngressSpec

NAME = "my-name"
NAMESPACE = "my-namespace"
POST_URI = Ingress._meta.create_url.format(namespace=NAMESPACE)
PUT_URI = Ingress._meta.update_url.format(name=NAME, namespace=NAMESPACE)
GET_URI = Ingress._meta.get_url.format(name=NAME, namespace=NAMESPACE)


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

        pytest.helpers.assert_any_call(post, POST_URI, call_params)

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
        pytest.helpers.assert_any_call(put, PUT_URI, call_params)


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "extensions/v1beta1",
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
            "selfLink": GET_URI,
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "spec": {
            'tls': [],
            'rules': [
                {
                    'host': 'old-dummy.example.com',
                    'http': {
                        'paths': [
                            {
                                'path': '/',
                                'backend': {
                                    'serviceName': 'dummy',
                                    'servicePort': 'http'
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
    ingress_backend = IngressBackend(serviceName="dummy", servicePort="http")
    http_ingress_path = HTTPIngressPath(path="/", backend=ingress_backend)
    http_ingress_rule = HTTPIngressRuleValue(paths=[http_ingress_path])
    ingress_rule = IngressRule(host="dummy.example.com", http=http_ingress_rule)
    ingress_spec = IngressSpec(rules=[ingress_rule])
    ingress = Ingress(metadata=object_meta, spec=ingress_spec)
    return ingress
