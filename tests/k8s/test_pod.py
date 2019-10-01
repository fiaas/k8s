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

from __future__ import absolute_import, unicode_literals

import mock
import pytest

from k8s.client import NotFound
from k8s.models.common import ObjectMeta
from k8s.models.pod import Pod, ContainerPort, Container, LocalObjectReference, PodSpec, Volume, VolumeMount, \
    SecretVolumeSource

NAME = "my-name"
NAMESPACE = "my-namespace"
POD_URI = Pod._meta.url_template.format(name="", namespace=NAMESPACE)


@pytest.mark.usefixtures("logger", "k8s_config")
class TestPod(object):
    def test_create_blank_pod(self):
        pod = _create_pod()
        assert pod.metadata.name == NAME
        assert pod.as_dict()["metadata"]["name"] == NAME

    def test_pod_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        pod = _create_pod()
        call_params = pod.as_dict()
        post.return_value.json.return_value = call_params

        assert pod._new
        pod.save()
        assert not pod._new
        pytest.helpers.assert_any_call(post, POD_URI, call_params)

    def test_get_or_create_pod_not_new(self, put, get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'creationTimestamp': '2017-10-03T10:36:20Z',
                'labels': {
                    'app': 'my-name', 'test': 'true'
                },
                'name': 'my-name',
                'namespace': 'my-namespace',
                'resourceVersion': '852',
                'selfLink': '/api/v1/namespaces/my-namespace/pods/my-name',
                'uid': 'b1e35ab5-a826-11e7-ba76-0800273598c9'
            },
            'spec': {
                'containers': [{
                    'image': 'dummy_image',
                    'imagePullPolicy': 'IfNotPresent',
                    'name': 'container',
                    'ports': [{
                        'containerPort': 5000,
                        'name': 'http5000',
                        'protocol': 'TCP'
                    }],
                    'resources': {},
                    'volumeMounts': [{
                        'mountPath': '/var/run/secrets/kubernetes.io/kubernetes-secrets',
                        'name': 'my-name',
                        'readOnly': True
                    }, {
                        'mountPath': '/var/run/secrets/kubernetes.io/serviceaccount',
                        'name': 'default-token-0g73b',
                        'readOnly': True
                    }]
                }],
                'imagePullSecrets': [{
                    'name': 'image_pull_secret'
                }],
                'restartPolicy': 'Always',
                'serviceAccount': 'default',
                'serviceAccountName': 'default',
                'terminationGracePeriodSeconds': 30,
                'volumes': [{
                    'name': 'my-name',
                    'secret': {
                        'defaultMode': 420,
                        'secretName': 'my-name'
                    }}, {
                    'name': 'default-token-0g73b',
                    'secret': {
                        'defaultMode': 420,
                        'secretName': 'default-token-0g73b'
                    }}]
            },
            'status': {
                'conditions': [{
                    'lastProbeTime': None,
                    'lastTransitionTime': '2017-10-03T10:36:20Z',
                    'status': 'True',
                    'type': 'PodScheduled'
                }],
                'phase': 'Pending',
                'qosClass': 'BestEffort'
            }
        }
        get.return_value = mock_response
        pod = Pod.get(name=NAME, namespace=NAMESPACE)
        assert not pod._new
        assert pod.metadata.name == NAME
        assert pod.spec.containers[0].ports[0].name == "http5000"
        call_params = pod.as_dict()
        put.return_value.json.return_value = call_params

        pod.save()
        pytest.helpers.assert_any_call(put, POD_URI + NAME, call_params)

    def test_pod_deleted(self, delete):
        Pod.delete(NAME, NAMESPACE)

        # call delete with service_name
        pytest.helpers.assert_any_call(delete, POD_URI + NAME)


def _create_pod():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true", "app": NAME})
    container_port = ContainerPort(name="http5000", containerPort=5000)
    secrets_volume_mounts = [
        VolumeMount(name=NAME, readOnly=True, mountPath="/var/run/secrets/kubernetes.io/kubernetes-secrets")]
    secret_volumes = [Volume(name=NAME, secret=SecretVolumeSource(secretName=NAME))]
    container = Container(name="container", image="dummy_image", ports=[container_port],
                          volumeMounts=secrets_volume_mounts)
    image_pull_secret = LocalObjectReference(name="image_pull_secret")
    pod_spec = PodSpec(containers=[container], imagePullSecrets=[image_pull_secret],
                       volumes=secret_volumes, serviceAccountName="default")
    first = Pod(metadata=object_meta, spec=pod_spec)
    return first
