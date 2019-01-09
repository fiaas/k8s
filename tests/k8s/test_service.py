#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import ServicePort, ServiceSpec, Service

NAMESPACE = 'my-namespace'
NAME = 'my_name'
POST_URI = Service._meta.create_url.format(namespace=NAMESPACE)
PUT_URI = Service._meta.update_url.format(name=NAME, namespace=NAMESPACE)
DELETE_URI = Service._meta.delete_url.format(name=NAME, namespace=NAMESPACE)
GET_URI = Service._meta.get_url.format(name=NAME, namespace=NAMESPACE)


@pytest.mark.usefixtures("k8s_config")
class TestService(object):
    def test_create_blank_service(self):
        svc = create_default_service()
        assert svc.metadata.name == NAME
        assert svc.as_dict()[u"metadata"][u"name"] == NAME

    def test_create_blank_object_meta(self):
        meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"label": "value"})
        assert not hasattr(meta, "_name")
        assert meta.name == NAME
        assert meta.namespace == NAMESPACE
        assert meta.labels == {"label": "value"}
        assert meta.as_dict() == {
            "name": NAME,
            "namespace": NAMESPACE,
            "finalizers": [],
            "labels": {
                "label": "value"
            },
            "ownerReferences": []
        }

    def test_service_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        service = create_default_service()
        call_params = service.as_dict()
        post.return_value.json.return_value = call_params

        assert service._new
        service.save()
        assert not service._new
        pytest.helpers.assert_any_call(post, POST_URI, call_params)

    def test_get_or_create_service_not_new(self, put, get):
        service = create_default_service()

        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "kind": "Service", "apiVersion": "v1", "metadata": {
                "name": NAME,
                "namespace": NAMESPACE,
                "selfLink": GET_URI,
                "uid": "cc562581-cbf5-11e5-b6ef-247703d2e388",
                "resourceVersion": "817",
                "creationTimestamp": "2016-02-05T10:47:06Z",
                "labels": {
                    "app": "test"
                },
            },
            "spec": {
                "ports": [
                    {
                        "name": "my-port", "protocol": "TCP", "port": 80, "targetPort": "name"
                    }
                ],
                "clusterIP": "10.0.0.54", "type": "ClusterIP", "sessionAffinity": "None"
            },
            "status": {
                "loadBalancer": {}
            }
        }
        get.return_value = mock_response

        metadata = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"app": "test"})
        port = ServicePort(name="my-port", port=80, targetPort="name")
        spec = ServiceSpec(ports=[port])

        from_api = Service.get_or_create(metadata=metadata, spec=spec)
        assert not from_api._new
        assert from_api.metadata.labels
        assert from_api.metadata.name == service.metadata.name
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, PUT_URI, call_params)

    def test_service_deleted(self, delete):
        Service.delete(NAME, NAMESPACE)

        # call delete with service_name
        pytest.helpers.assert_any_call(delete, DELETE_URI)

    def test_list_services(self, get):
        service_list = {
            "apiVersion": "v1",
            "kind": "List",
            "metadata": {},
            "resourceVersion": "",
            "selflink": "",
            "items": [
                {
                    "kind": "Service",
                    "apiVersion": "v1",
                    "metadata": {
                        "name": "foo",
                        "namespace": "default",
                        "selfLink": "/api/v1/namespaces/default/services/foo",
                        "uid": "cc562581-cbf5-11e5-b6ef-247703d2e388",
                        "resourceVersion": "817",
                        "creationTimestamp": "2016-02-05T10:47:06Z",
                    },
                    "spec": {
                        "ports": [
                            {
                                "name": "https", "protocol": "TCP", "port": 443, "targetPort": "https"
                            }
                        ],
                        "clusterIP": "10.0.0.1", "type": "ClusterIP", "sessionAffinity": "None"
                    },
                    "status": {
                        "loadBalancer": {}
                    }
                },
                {
                    "kind": "Service",
                    "apiVersion": "v1",
                    "metadata": {
                        "name": "bar",
                        "namespace": "default",
                        "selfLink": "/api/v1/namespaces/default/services/bar",
                        "uid": "4d00cb9e-30d2-11e7-ba70-7a4531eb635c",
                        "resourceVersion": "13608",
                        "creationTimestamp": "2017-05-04T14:02:25Z",
                    },
                    "spec": {
                        "ports": [
                            {
                                "name": "http", "protocol": "TCP", "port": 80, "targetPort": "8080"
                            }
                        ],
                        "clusterIP": "10.0.0.2", "type": "ClusterIP", "sessionAffinity": "None"
                    },
                    "status": {
                        "loadBalancer": {}
                    }
                }
            ]
        }
        mock_response = mock.Mock()
        mock_response.json.return_value = service_list
        get.return_value = mock_response

        services = Service.list(namespace="default")
        assert services[0].metadata.name == "foo"
        assert services[0].metadata.namespace == "default"
        assert services[0].spec.ports[0].name == "https"
        assert services[0].spec.ports[0].port == 443
        assert services[0].spec.ports[0].targetPort == "https"
        assert services[1].metadata.name == "bar"
        assert services[1].metadata.namespace == "default"
        assert services[1].spec.ports[0].name == "http"
        assert services[1].spec.ports[0].port == 80
        assert services[1].spec.ports[0].targetPort == "8080"


def create_default_service():
    metadata = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"app": "test"})
    port = ServicePort(name="my-port", port=80, targetPort="name")
    spec = ServiceSpec(ports=[port])
    return Service(metadata=metadata, spec=spec)


def create_simple_http_service_spec():
    return ServiceSpec(type="http")
