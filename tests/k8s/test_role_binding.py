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
from k8s.models.role_binding import RoleBinding, RoleRef, Subject

NAME = "my-role-binding"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestRoleBinding(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        role_binding = _create_default_role_binding()
        call_params = role_binding.as_dict()
        post.return_value.json.return_value = call_params

        assert role_binding._new
        role_binding.save()
        assert not role_binding._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        role_binding = _create_default_role_binding()

        from_api = RoleBinding.get_or_create(
            metadata=role_binding.metadata,
            roleRef=role_binding.roleRef,
            subjects=role_binding.subjects,
        )
        assert not from_api._new
        assert from_api.roleRef == role_binding.roleRef
        assert from_api.subjects == role_binding.subjects

    def test_deleted(self, delete):
        RoleBinding.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
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
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "Role",
            "name": "my-role",
        },
        "subjects": [
            {
                "kind": "ServiceAccount",
                "name": "my-service-account",
                "namespace": "default",
            },
        ],
    }
    return mock_response


def _create_default_role_binding():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    role_ref = RoleRef(apiGroup=["rbac.authorization.k8s.io"], kind=["Role"], name=["my-role"])
    subject = Subject(kind="ServiceAccount", name="my-service-account", namespace="default")
    return RoleBinding(metadata=object_meta, roleRef=role_ref, subjects=[subject])


def _uri(namespace, name=""):
    uri = "/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}"
    return uri.format(name=name, namespace=namespace)
