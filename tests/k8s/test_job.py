#!/usr/bin/env python
# -*- coding: utf-8

import mock
import pytest

from k8s.client import NotFound
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import Container, LocalObjectReference, PodSpec, PodTemplateSpec
from k8s.models.v1_6.kubernetes.apis.batch.v1 import Job, JobSpec

NAME = "my-name"
NAMESPACE = "my-namespace"
POST_URI = Job._meta.create_url.format(namespace=NAMESPACE)


@pytest.mark.usefixtures("k8s_config")
class TestJobs(object):
    def test_create_blank_job(self):
        object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE)
        job = Job(metadata=object_meta)
        assert job.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        job = _create_default_job()
        call_params = job.as_dict()
        post.return_value.json.return_value = call_params

        assert job._new
        job.save()
        assert not job._new

        pytest.helpers.assert_any_call(post, POST_URI, call_params)


def _create_default_job():
    labels = {"test": "true"}
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels=labels)
    container = Container(
        name="container",
        image="dummy_image"
    )
    image_pull_secret = LocalObjectReference(name="image_pull_secret")
    pod_spec = PodSpec(containers=[container], imagePullSecrets=[image_pull_secret], serviceAccountName="default",
                       restartPolicy="Never")
    pod_template_spec = PodTemplateSpec(metadata=object_meta, spec=pod_spec)
    job_spec = JobSpec(template=pod_template_spec)
    job = Job(metadata=object_meta, spec=job_spec)

    return job


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
    return mock_response
