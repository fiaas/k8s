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
from k8s.models.policy_v1_pod_disruption_budget import PodDisruptionBudget, PodDisruptionBudgetSpec, LabelSelector

NAME = "my-pod-disruption-budget"
NAMESPACE = "my-namespace"


# pylint: disable=R0201
@pytest.mark.usefixtures("k8s_config")
class TestPodDisruptionBudget(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        pdb = _create_default_pdb()
        call_params = pdb.as_dict()
        post.return_value.json.return_value = call_params

        assert pdb._new
        pdb.save()
        assert not pdb._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        pdb = _create_default_pdb()

        from_api = PodDisruptionBudget.get_or_create(
            metadata=pdb.metadata,
            spec=pdb.spec,
        )
        assert not from_api._new
        assert from_api.spec == pdb.spec

    def test_deleted(self, delete):
        PodDisruptionBudget.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "policy/v1",
        "kind": "PodDisruptionBudget",
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
            "minAvailable": 1,
            "selector": {
                "matchLabels": {
                    "application": "my-app",
                },
            },
        },
    }
    return mock_response


def _create_default_pdb():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    selector = LabelSelector(matchLabels={"app": "my-app"})
    spec = PodDisruptionBudgetSpec(maxUnavailable=1, selector=selector)
    return PodDisruptionBudget(metadata=object_meta, spec=spec)


def _uri(namespace, name=""):
    uri = "/apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}"
    return uri.format(name=name, namespace=namespace)
