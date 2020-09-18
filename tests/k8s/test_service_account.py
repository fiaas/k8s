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
from k8s.models.common import ObjectMeta, LocalObjectReference
from k8s.models.service_account import ServiceAccount

NAME = "my-service-account"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestServiceAccount(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        service_account = _create_default_service_account()
        call_params = service_account.as_dict()
        post.return_value.json.return_value = call_params

        assert service_account._new
        service_account.save()
        assert not service_account._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        service_account = _create_default_service_account()

        from_api = ServiceAccount.get_or_create(
            metadata=service_account.metadata,
            secrets=service_account.secrets,
            imagePullSecrets=service_account.imagePullSecrets,
            automountServiceAccountToken=service_account.automountServiceAccountToken
        )
        assert not from_api._new
        assert from_api.secrets == service_account.secrets

        from_api.secrets = [LocalObjectReference(name="my-other-secret")]
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)

    def test_deleted(self, delete):
        ServiceAccount.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
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
        'automountServiceAccountToken': "true",
        'secrets': [{
            'name': 'my-secret'
        }],
        'imagePullSecrets': [{
            'name': 'my-image-pull-secret'
        }]
    }
    return mock_response


def _create_default_service_account():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    secrets = [LocalObjectReference(name="my-secret")]
    image_pull_secrets = [LocalObjectReference(name="my-image-pull-secret")]
    automount_service_account_token = True

    service_account = ServiceAccount(metadata=object_meta)
    service_account.secrets = secrets
    service_account.imagePullSecrets = image_pull_secrets
    service_account.automountServiceAccountToken = automount_service_account_token

    return service_account


def _uri(namespace, name=""):
    return "/api/v1/namespaces/{namespace}/serviceaccounts/{name}".format(name=name, namespace=namespace)
