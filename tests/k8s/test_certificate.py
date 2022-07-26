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
from k8s.models.certificate import Certificate, CertificateSpec, CertificateStatus, \
    IssuerReference, CertificateCondition

NAME = "my-name"
NAMESPACE = "my-namespace"
REF_NAME = "example_tls"


# pylint: disable=R0201
@pytest.mark.usefixtures("k8s_config")
class TestCertificate(object):
    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        cert = _create_default_certificate()
        call_params = cert.as_dict()
        post.return_value.json.return_value = call_params

        assert cert._new
        cert.save()
        assert not cert._new

        pytest.helpers.assert_any_call(post, _uri(NAMESPACE), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        cert = _create_default_certificate()

        from_api = Certificate.get_or_create(metadata=cert.metadata, spec=cert.spec, status=cert.status)
        assert not from_api._new
        assert from_api.spec.secretName == REF_NAME

        from_api.data = {"boo": "baz"}
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAMESPACE, NAME), call_params)

    def test_deleted(self, delete):
        Certificate.delete(NAME, namespace=NAMESPACE)
        pytest.helpers.assert_any_call(delete, _uri(NAMESPACE, NAME))


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "cert-manager.io/v1",
        "kind": "Certificate",
        "metadata": {
            "creationTimestamp": "2022-05-01T13:37:00Z",
            "generation": 1,
            "labels": {
                "test": "true"
            },
            "name": NAME,
            "namespace": NAMESPACE,
            "resourceVersion": "178",
            "selfLink": _uri(NAMESPACE, NAME),
            "uid": "51ae75dc-c3fc-4b08-842f-1d546b88ae98"
        },
        "spec": {
            "secretName": REF_NAME,
            "issuerRef": {
                "name": "test",
                "kind": "Issuer"
            }
        },
        "status": {
            "conditions": [
                {
                    "type": "Ready",
                    "status": "True"
                }
            ]
        },
    }
    return mock_response


def _create_default_certificate():
    object_meta = ObjectMeta(name=NAME, namespace=NAMESPACE, labels={"test": "true"})
    spec = CertificateSpec(secretName=REF_NAME, issuerRef=IssuerReference(name="test", kind="Issuer"))
    status = CertificateStatus(conditions=[CertificateCondition(type="Ready", status="True")])
    cert = Certificate(metadata=object_meta, spec=spec, status=status)
    return cert


def _uri(namespace, name=""):
    uri = "/apis/cert-manager.io/v1/namespaces/{namespace}/certificates/{name}"
    return uri.format(name=name, namespace=namespace)
