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
from k8s.models.role import Role, PolicyRule

NAME = "my-role"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestRole(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        role = _create_default_role()
        call_params = role.as_dict()
        post.return_value.json.return_value = call_params

        assert role._new
        role.save()
        assert not role._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        role = _create_default_role()

        from_api = Role.get_or_create(
            metadata=role.metadata,
            rules=role.rules,
        )
        assert not from_api._new
        assert from_api.rules == role.rules

    def test_deleted(self, delete):
        Role.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
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
        "rules": [
            {
                "apiGroups": ["fiaas.schibsted.io"],
                "resources": ["applications", "application-statuses"],
                "verbs": ["get", "list", "watch"],
            },
        ],
    }
    return mock_response


def _create_default_role():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    policy_rules = [
        PolicyRule(
            apiGroups=["fiaas.schibsted.io"],
            resources=["applications", "application-statuses"],
            verbs=["get", "list", "watch"],
            resourceNames=[],
            nonResourceURLs=[],
        )
    ]
    return Role(metadata=object_meta, rules=policy_rules)


def _uri(namespace, name=""):
    uri = "/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/roles/{name}"
    return uri.format(name=name, namespace=namespace)
