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
from k8s.models.apiextensions_v1_custom_resource_definition import (
    CustomResourceConversion, CustomResourceDefinition, CustomResourceDefinitionNames,
    CustomResourceDefinitionSpec, CustomResourceDefinitionVersion, JSONSchemaProps)

NAME = "my-name"


# pylint: disable=R0201
@pytest.mark.usefixtures("k8s_config")
class TestCustomResourceDefinition(object):
    def test_create_blank(self):
        object_meta = ObjectMeta(name=NAME, labels={"test": "true"})
        crd = CustomResourceDefinition(metadata=object_meta)
        assert crd.as_dict()[u"metadata"][u"name"] == NAME

    def test_created_if_not_exists(self, post, api_get):
        api_get.side_effect = NotFound()
        crd = _create_default_crd()
        call_params = crd.as_dict()
        post.return_value.json.return_value = call_params

        assert crd._new
        crd.save()
        assert not crd._new

        pytest.helpers.assert_any_call(post, _uri(), call_params)

    def test_updated_if_exists(self, get, put):
        mock_response = _create_mock_response()
        get.return_value = mock_response
        crd = _create_default_crd()

        from_api = CustomResourceDefinition.get_or_create(metadata=crd.metadata, spec=crd.spec)
        assert not from_api._new
        call_params = from_api.as_dict()
        put.return_value.json.return_value = call_params

        from_api.save()
        pytest.helpers.assert_any_call(put, _uri(NAME), call_params)

    def test_nested_json_schema_props(self, put):
        crd_dict = _json_schema_props_crd_dict()
        crd = CustomResourceDefinition.from_dict(crd_dict)

        call_params = crd.as_dict()
        put.return_value.json.return_value = call_params

        assert isinstance(crd.spec.versions[0].schema.openAPIV3Schema, JSONSchemaProps)
        assert isinstance(crd.spec.versions[0].schema.openAPIV3Schema._not, JSONSchemaProps)

        crd.save()
        pytest.helpers.assert_any_call(put, _uri(NAME), call_params)

    def test_json_schema_props_any_field(self, put):
        for default in [42, "string", True, [], {}]:
            crd_dict = _json_schema_props_crd_dict(default)
            crd = CustomResourceDefinition.from_dict(crd_dict)

            call_params = crd.as_dict()
            put.return_value.json.return_value = call_params

            assert isinstance(crd.spec.versions[0].schema.openAPIV3Schema.default, type(default))

            crd.save()
            pytest.helpers.assert_any_call(put, _uri(NAME), call_params)


def _json_schema_props_crd_dict(default=None):
    return {
        "apiVersion": "apiextensions.k8s.io/v1",
        "kind": "CustomResourceDefinition",
        "metadata": {
            "creationTimestamp": "2019-11-23T13:43:42Z",
            "generation": 7,
            "labels": {
                "test": "true"
            },
            "name": NAME,
            "resourceVersion": "96758807",
            "selfLink": _uri(NAME),
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "spec": {
            "conversion": {"strategy": "None"},
            "group": "example.com",
            "names": {
                "kind": "MyCustomResource",
                "plural": "mycustomresources"
            },
            "scope": "namespaced",
            "versions": [{
                "name": "v1",
                "served": True,
                "schema": {
                    "openAPIV3Schema": {
                        "type": "object",
                        "properties": {
                            "spec": {
                                "type": "object",
                                "properties": {
                                    "cronSpec": {
                                        "type": "string"
                                    },
                                    "image": {
                                        "type": "string"
                                    },
                                    "replicas": {
                                        "type": "integer"
                                    }
                                }
                            }
                        },
                        "not": {
                            "type": "integer",
                        },
                        "default": default
                    }
                }
            }]
        }
    }


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "apiextensions.k8s.io/v1",
        "kind": "CustomResourceDefinition",
        "metadata": {
            "creationTimestamp": "2019-11-23T13:43:42Z",
            "generation": 7,
            "labels": {
                "test": "true"
            },
            "name": NAME,
            "resourceVersion": "96758807",
            "selfLink": _uri(NAME),
            "uid": "d8f1ba26-b182-11e6-a364-fa163ea2a9c4"
        },
        "spec": {
            "conversion": {"strategy": "None"},
            "group": "example.com",
            "names": {
                "kind": "MyCustomResource",
                "plural": "mycustomresources"
            },
            "scope": "namespaced",
            "versions": [{
                "name": "v1",
                "served": True
            }]
        }
    }
    return mock_response


def _create_default_crd():
    object_meta = ObjectMeta(name=NAME, labels={"test": "true"})
    spec = CustomResourceDefinitionSpec(
        conversion=CustomResourceConversion(strategy="None"),
        group="example.com",
        names=CustomResourceDefinitionNames(kind="MyCustomResource", plural="mycustomresources"),
        scope="Namespaced",
        versions=[CustomResourceDefinitionVersion(name="v42", served=True)]
    )
    crd = CustomResourceDefinition(metadata=object_meta, spec=spec)
    return crd


def _uri(name=""):
    return "/apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}".format(name=name)
