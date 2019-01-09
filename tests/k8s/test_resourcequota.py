#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.enums import ResourceQuotaScope
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import ResourceQuota, ResourceQuotaSpec

NAME = "my-name"
NAMESPACE = "my-namespace"
POST_URI = ResourceQuota._meta.create_url.format(namespace=NAMESPACE)
PUT_URI = ResourceQuota._meta.update_url.format(name=NAME, namespace=NAMESPACE)
DELETE_URI = ResourceQuota._meta.delete_url.format(name=NAME, namespace=NAMESPACE)
GET_URI = ResourceQuota._meta.get_url.format(name=NAME, namespace=NAMESPACE)


@pytest.mark.usefixtures("k8s_config")
class TestResourceQuota(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        resourcequota = _create_default_resourcequota()
        call_params = resourcequota.as_dict()
        post.return_value.json.return_value = call_params

        assert resourcequota._new
        resourcequota.save()
        assert not resourcequota._new

        pytest.helpers.assert_any_call(post, POST_URI, call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        resourcequota = _create_default_resourcequota()

        from_api = ResourceQuota.get_or_create(metadata=resourcequota.metadata, spec=resourcequota.spec)
        assert not from_api._new
        assert from_api.spec == resourcequota.spec
        assert from_api.status == resourcequota.status

        from_api.spec = ResourceQuotaSpec(hard={'pods': "10"}, scopes=[ResourceQuotaScope.BestEffort])
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, PUT_URI, call_params)

    def test_deleted(self, delete):
        ResourceQuota.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, DELETE_URI)


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "v1",
        "kind": "ResourceQuota",
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
        "spec": {
            "hard": {
                "pods": "0",
            },
            "scopes": [
                ResourceQuotaScope.NotBestEffort,
            ],
        },
    }
    return mock_response


def _create_default_resourcequota():
    objectmeta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    resourcequotaspec = ResourceQuotaSpec(hard={"pods": "0"}, scopes=[ResourceQuotaScope.NotBestEffort])
    resourcequota = ResourceQuota(metadata=objectmeta, spec=resourcequotaspec)
    return resourcequota
