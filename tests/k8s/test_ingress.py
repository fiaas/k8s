#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.common import ObjectMeta
from k8s.models.ingress import Ingress, IngressSpec, IngressRule, IngressBackend, HTTPIngressPath, HTTPIngressRuleValue

NAME = "my-name"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestIngress(object):
    @pytest.fixture
    def post(self):
        with mock.patch('k8s.client.Client.post') as m:
            yield m

    @pytest.fixture
    def put(self):
        with mock.patch('k8s.client.Client.put') as m:
            yield m

    @pytest.fixture
    def get(self):
        with mock.patch('k8s.client.Client.get') as m:
            yield m

    @pytest.fixture
    def api_get(self):
        with mock.patch('k8s.base.ApiMixIn.get') as m:
            yield m

    def test_create_blank(self):
        object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
        ingress = Ingress(metadata=object_meta)
        assert ingress.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        ingress = _create_default_ingress()
        call_params = ingress.as_dict()

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

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)


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
            "selfLink": _uri(NAMESPACE, NAME),
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


def _uri(namespace, name=""):
    return "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}".format(name=name, namespace=namespace)
