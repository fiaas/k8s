#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2022 The FIAAS Authors
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
from k8s.models.secret import Secret

NAME = "my-name"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestSecret(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        secret = _create_default_secret()
        call_params = secret.as_dict()
        post.return_value.json.return_value = call_params

        assert secret._new
        secret.save()
        assert not secret._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        secret = _create_default_secret()

        from_api = Secret.get_or_create(metadata=secret.metadata, data=secret.data, type=secret.type)
        assert not from_api._new
        assert from_api.data == {"foo": "bar"}

        from_api.data = {"baz": "quux"}
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)

    def test_deleted(self, delete):
        Secret.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "v1",
        "kind": "Secret",
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
        "data": {
            "foo": "bar",
        },
        "type": "kubernetes.io/tls",
    }
    return mock_response


def _create_default_secret():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    data = {"foo": "bar"}
    type = "kubernetes.io/tls"
    secret = Secret(metadata=object_meta, data=data, type=type)
    return secret


def _uri(namespace, name=""):
    return "/api/v1/namespaces/{namespace}/secrets/{name}".format(name=name, namespace=namespace)
