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
from k8s.models.resourcequota import ResourceQuota, ResourceQuotaSpec, NotBestEffort, BestEffort

NAME = "my-name"
NAMESPACE = "my-namespace"


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

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        resourcequota = _create_default_resourcequota()

        from_api = ResourceQuota.get_or_create(metadata=resourcequota.metadata, spec=resourcequota.spec)
        assert not from_api._new
        assert from_api.spec == resourcequota.spec
        assert from_api.status == resourcequota.status

        from_api.spec = ResourceQuotaSpec(hard={'pods': "10"}, scopes=[BestEffort])
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)

    def test_deleted(self, delete):
        ResourceQuota.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


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
            "selfLink": _uri(NAMESPACE, NAME),
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "spec": {
            "hard": {
                "pods": "0",
            },
            "scopes": [
                NotBestEffort,
            ],
        },
    }
    return mock_response


def _create_default_resourcequota():
    objectmeta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    resourcequotaspec = ResourceQuotaSpec(hard={"pods": "0"}, scopes=[NotBestEffort])
    resourcequota = ResourceQuota(metadata=objectmeta, spec=resourcequotaspec)
    return resourcequota


def _uri(namespace, name=""):
    return "/api/v1/namespaces/{namespace}/resourcequotas".format(name=name, namespace=namespace)
