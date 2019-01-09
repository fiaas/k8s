#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import ConfigMap

NAME = "my-name"
NAMESPACE = "my-namespace"
POST_URI = ConfigMap._meta.create_url.format(namespace=NAMESPACE)
PUT_URI = ConfigMap._meta.update_url.format(name=NAME, namespace=NAMESPACE)
DELETE_URI = ConfigMap._meta.delete_url.format(name=NAME, namespace=NAMESPACE)
GET_URI = ConfigMap._meta.get_url.format(name=NAME, namespace=NAMESPACE)


@pytest.mark.usefixtures("k8s_config")
class TestConfigMap(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        configmap = _create_default_configmap()
        call_params = configmap.as_dict()
        post.return_value.json.return_value = call_params

        assert configmap._new
        configmap.save()
        assert not configmap._new

        pytest.helpers.assert_any_call(post, POST_URI, call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        configmap = _create_default_configmap()

        from_api = ConfigMap.get_or_create(metadata=configmap.metadata, data=configmap.data)
        assert not from_api._new
        assert from_api.data == {"foo": "bar"}

        from_api.data = {"baz": "quux"}
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, PUT_URI, call_params)

    def test_deleted(self, delete):
        ConfigMap.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, DELETE_URI)


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "creationTimestamp": "2017-09-08T13:37:00Z",
            "generation": 1,
            "labels": {
                "test": "true"
            },
            "name": NAME,
            "namespace": NAMESPACE,
            "resourceVersion": "42",
            "selfLink": GET_URI,
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "data": {
            "foo": "bar",
        },
    }
    return mock_response


def _create_default_configmap():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    data = {"foo": "bar"}
    configmap = ConfigMap(metadata=object_meta, data=data)
    return configmap
