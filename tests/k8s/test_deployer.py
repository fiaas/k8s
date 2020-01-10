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
from six import u

from k8s.client import NotFound
from k8s.models.common import ObjectMeta
from k8s.models.deployment import Deployment, DeploymentSpec, LabelSelector, RollingUpdateDeployment, \
    DeploymentStrategy
from k8s.models.pod import ContainerPort, Container, LocalObjectReference, Probe, HTTPGetAction, TCPSocketAction, \
    PodTemplateSpec, PodSpec

NAME = "my-name"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestDeployer(object):
    def test_create_blank_deployment(self):
        object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE)
        deployment = Deployment(metadata=object_meta)
        assert deployment.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        deployment = _create_default_deployment()
        call_params = deployment.as_dict()
        post.return_value.json.return_value = call_params

        assert deployment._new
        deployment.save()
        assert not deployment._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_created_if_not_exists_with_percentage_rollout_strategy(self, post, api_get):
        api_get.side_effect = NotFound()
        deployment = _create_default_deployment()
        rolling_update = RollingUpdateDeployment(maxUnavailable=u("50%"), maxSurge=u("50%"))
        deployment.spec.strategy = DeploymentStrategy(type="RollingUpdate", rollingUpdate=rolling_update)
        call_params = deployment.as_dict()
        post.return_value.json.return_value = call_params

        assert deployment._new
        deployment.save()
        assert not deployment._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        deployment = _create_default_deployment()

        from_api = Deployment.get_or_create(metadata=deployment.metadata, spec=deployment.spec)
        assert not from_api._new
        assert from_api.spec.replicas == 2
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)

    def test_delete(self, delete):
        Deployment.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_default_deployment():
    labels = {"test": "true"}
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels=labels)
    container_port = ContainerPort(name="http5000", containerPort=5000)
    http = HTTPGetAction(path="/", port="http5000")
    liveness = Probe(httpGet=http)
    tcp = TCPSocketAction(port=5000)
    readiness = Probe(tcpSocket=tcp)
    container = Container(
        name="container",
        image="dummy_image",
        ports=[container_port],
        livenessProbe=liveness,
        readinessProbe=readiness
    )
    image_pull_secret = LocalObjectReference(name="image_pull_secret")
    pod_spec = PodSpec(containers=[container], imagePullSecrets=[image_pull_secret], serviceAccountName="default")
    pod_template_spec = PodTemplateSpec(metadata=object_meta, spec=pod_spec)
    deployer_spec = DeploymentSpec(replicas=2, selector=LabelSelector(matchLabels=labels),
                                   template=pod_template_spec, revisionHistoryLimit=5)
    deployment = Deployment(metadata=object_meta, spec=deployer_spec)

    return deployment


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        u"metadata": {
            u"labels": {
                u"test": u"true"
            },
            u"namespace": u"my-namespace",
            u"name": u"my-name"
        },
        u"spec": {
            u"replicas": 2,
            u"revisionHistoryLimit": 5,
            u"template": {
                u"spec": {
                    u"dnsPolicy": u"ClusterFirst",
                    u"serviceAccountName": u"default",
                    u"restartPolicy": u"Always",
                    u"volumes": [],
                    u"imagePullSecrets": [
                        {
                            u"name": u"image_pull_secret"
                        }
                    ],
                    u"containers": [
                        {
                            u"livenessProbe": {
                                u"initialDelaySeconds": 5,
                                u"httpGet": {
                                    u"path": u"/",
                                    u"scheme": u"HTTP",
                                    u"port": u"http5000"
                                }
                            },
                            u"name": u"container",
                            u"image": u"dummy_image",
                            u"volumeMounts": [],
                            u"env": [],
                            u"imagePullPolicy": u"IfNotPresent",
                            u"readinessProbe": {
                                u"initialDelaySeconds": 5,
                                u"tcpSocket": {
                                    u"port": 5000
                                }
                            },
                            u"ports": [
                                {
                                    u"protocol": u"TCP",
                                    u"containerPort": 5000,
                                    u"name": u"http5000"
                                }
                            ]
                        }
                    ]
                },
                u"metadata": {
                    u"labels": {
                        u"test": u"true"
                    },
                    u"namespace": u"my-namespace",
                    u"name": u"my-name"
                }
            },
            u"selector": {
                u"matchLabels": {
                    u"test": u"true"
                }
            }
        }
    }
    return mock_response


def _uri(namespace, name=""):
    return "/apis/apps/v1/namespaces/{namespace}/deployments/{name}".format(name=name, namespace=namespace)
