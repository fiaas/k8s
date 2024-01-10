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
from k8s.models.common import ObjectMeta, LabelSelector
from k8s.models.policy_v1_pod_disruption_budget import PodDisruptionBudget, PodDisruptionBudgetSpec

NAME = "my-name"
NAMESPACE = "my-namespace"
PDB_URI = PodDisruptionBudget._meta.url_template.format(name="", namespace=NAMESPACE)


@pytest.mark.usefixtures("logger", "k8s_config")
class TestPodDisruptionBudget(object):
    def test_create_blank_pdb(self):
        pdb = _create_pdb()
        assert pdb.metadata.name == NAME
        assert pdb.as_dict()["metadata"]["name"] == NAME

    def test_pdb_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        pdb = _create_pdb()
        call_params = pdb.as_dict()
        post.return_value.json.return_value = call_params

        assert pdb._new
        pdb.save()
        assert not pdb._new
        pytest.helpers.assert_any_call(post, PDB_URI, call_params)

    def test_get_or_create_pdb_not_new(self, put, get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'apiVersion': 'policy/v1',
            'kind': 'PodDisruptionBudget',
            'metadata': {
                'creationTimestamp': '2017-10-03T10:36:20Z',
                'labels': {
                    'app': 'my-name', 'test': 'true'
                },
                'name': 'my-name',
                'namespace': 'my-namespace',
                'resourceVersion': '852',
                'uid': 'b1e35ab5-a826-11e7-ba76-0800273598c9'
            },
            'spec': {
                'minAvailable': 1,
                'selector': {
                    'matchLabels': {
                        'app': 'my-name',
                    },
                },
            },
            'status': {
                'currentHealthy': 1,
                'desiredHealthy': 1,
                'disruptedPods': {},
                'expectedPods': 1,
                'observedGeneration': 1
            }
        }
        get.return_value = mock_response
        pdb = PodDisruptionBudget.get(name=NAME, namespace=NAMESPACE)
        assert not pdb._new
        assert pdb.metadata.name == NAME
        assert pdb.spec.minAvailable == 1
        assert pdb.spec.selector.matchLabels["app"] == NAME
        call_params = pdb.as_dict()
        put.return_value.json.return_value = call_params

        pdb.save()
        pytest.helpers.assert_any_call(put, PDB_URI + NAME, call_params)

    def test_pdb_deleted(self, delete):
        PodDisruptionBudget.delete(NAME, NAMESPACE)

        # call delete with service_name
        pytest.helpers.assert_any_call(delete, PDB_URI + NAME)


def _create_pdb():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true", "app": NAME})
    pdb_spec = PodDisruptionBudgetSpec(minAvailable=1, selector=LabelSelector(matchLabels={"app": NAME}))
    first = PodDisruptionBudget(metadata=object_meta, spec=pdb_spec)
    return first
