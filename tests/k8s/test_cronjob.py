#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2020 The FIAAS Authors
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
from k8s.models.cronjob import CronJob, CronJobSpec
from k8s.models.job import JobSpec, JobTemplateSpec
from k8s.models.pod import Container, PodTemplateSpec, PodSpec


NAME = "my-name"
NAMESPACE = "my-namespace"


@pytest.mark.usefixtures("k8s_config")
class TestCronJobs(object):
    def test_create_blank_job(self):
        object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE)
        cronjob = CronJob(metadata=object_meta)
        assert cronjob.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        cronjob = _create_default_cronjob()
        call_params = cronjob.as_dict()
        post.return_value.json.return_value = call_params

        assert cronjob._new
        cronjob.save()
        assert not cronjob._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)


def _create_default_cronjob():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE)
    container = Container(
        name="container",
        image="dummy_image"
    )
    pod_spec = PodSpec(containers=[container], serviceAccountName="default",
                       restartPolicy="OnFailure")
    pod_template_spec = PodTemplateSpec(metadata=object_meta, spec=pod_spec)
    job_spec = JobSpec(template=pod_template_spec)
    job_template_spec = JobTemplateSpec(metadata=object_meta, spec=job_spec)
    cronjob_spec = CronJobSpec(concurrencyPolicy="Allow", failedJobsHistoryLimit=0, jobTemplate=job_template_spec,
                               schedule="*/1 * * * *", startingDeadlineSeconds=5, successfulJobsHistoryLimit=100,
                               suspend=True)
    cronjob = CronJob(metadata=object_meta, spec=cronjob_spec)

    return cronjob


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
            u"schedule": u"*/1 * * * *",
            u"jobTemplate": {
                u"spec": {
                    u"template": {
                        u"spec": {
                            u"serviceAccountName": u"default",
                            u"restartPolicy": u"Never",
                            u"volumes": [],
                            u"imagePullSecrets": [
                                {
                                    u"name": u"image_pull_secret"
                                }
                            ],
                            u"containers": [
                                {
                                    u"name": u"container",
                                    u"image": u"dummy_image",
                                    u"volumeMounts": [],
                                    u"env": [],
                                    u"imagePullPolicy": u"IfNotPresent",
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
                    }
                }
            }
        }
    }
    return mock_response


def _uri(namespace, name=""):    
    return "/apis/batch/v1beta1/namespaces/{namespace}/cronjobs/{name}".format(name=name, namespace=namespace)
