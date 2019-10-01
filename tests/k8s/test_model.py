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

from __future__ import unicode_literals

import pytest
import six
from mock import create_autospec
from requests import Response

from k8s.base import Model
from k8s.client import Client
from k8s.fields import Field, ListField, OnceField, ReadOnlyField
from k8s.models.common import ObjectMeta


class ModelTest(Model):
    class Meta:
        pass

    metadata = Field(ObjectMeta)
    field = Field(int)
    list_field = ListField(int)
    once_field = OnceField(int)
    read_only_field = ReadOnlyField(int)
    alt_type_field = Field(int, alt_type=six.text_type)
    dict_field = Field(dict)
    _exec = Field(int)


@pytest.mark.usefixtures("logger")
class TestModel(object):
    @pytest.fixture()
    def mock_response(self, monkeypatch):
        mock_client = create_autospec(Client)
        mock_response = create_autospec(Response)
        monkeypatch.setattr(ModelTest, "_client", mock_client)
        mock_client.get.return_value = mock_response
        return mock_response

    def test_unexpected_kwargs(self):
        with pytest.raises(TypeError):
            ModelTest(unknown=3)

    def test_change(self, mock_response):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {"field": 1, "list_field": [1], "once_field": 1, "read_only_field": 1}
        instance = ModelTest.get_or_create(metadata=metadata, field=2, list_field=[2], once_field=2, read_only_field=2)
        assert instance.field == 2
        assert instance.list_field == [2]
        assert instance.once_field == 1
        assert instance.read_only_field == 1

    @pytest.mark.parametrize("value", (None, {}, {"key": "value"}), ids=("None", "Empty dict", "Key-Value"))
    def test_set_dict_field(self, mock_response, value):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {'dict_field': {'thing': 'otherthing'}}
        instance = ModelTest.get_or_create(metadata=metadata, dict_field=value)
        assert instance.dict_field == value

    @pytest.mark.parametrize("value", (None, [], [5, 6]), ids=("None", "Empty list", "2-item list"))
    def test_set_list_field_to_empty(self, mock_response, value):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {'list_field': [1, 2]}
        instance = ModelTest.get_or_create(metadata=metadata, list_field=value)
        assert instance.list_field == value

    def test_serialization_of_empty_dict(self):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        kwargs = {"dict_field": {}, "metadata": metadata}
        instance = ModelTest(**kwargs)
        d = instance.as_dict()
        assert "dict_field" not in d

    def test_serialization_of_empty_list(self):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        kwargs = {"list_field": [], "metadata": metadata}
        instance = ModelTest(**kwargs)
        d = instance.as_dict()
        assert d["list_field"] == []

    def test_annotations_replace(self, mock_response):
        mock_response.json.return_value = {
            "metadata": {
                "name": "my-name",
                "namespace": "my-namespace",
                "annotations": {
                    "must_discard": "this",
                    "will_overwrite": "this"
                }
            }
        }
        metadata = ObjectMeta(name="my-name", namespace="my-namespace", annotations={"will_overwrite": "that"})
        instance = ModelTest.get_or_create(metadata=metadata)
        assert instance.metadata.annotations["will_overwrite"] == "that"
        assert "must_discard" not in instance.metadata.annotations

    def test_spec_merge(self, mock_response):
        mock_response.json.return_value = {
            "metadata": {
                "name": "my-name",
                "namespace": "my-namespace",
                "generateName": "my-generated-name",
                "selfLink": "http://this.link.stays.example.com"
            }
        }
        metadata = ObjectMeta(name="my-name", namespace="my-namespace", generateName="my-new-generated-name")
        instance = ModelTest.get_or_create(metadata=metadata)
        assert instance.metadata.generateName == "my-new-generated-name"
        assert instance.metadata.selfLink == "http://this.link.stays.example.com"

    def test_independent_default_value(self):
        my_model1 = ModelTest()
        my_model1.list_field.append(1)

        my_model2 = ModelTest()
        my_model2.list_field.append(2)

        assert [1] == my_model1.list_field
        assert [2] == my_model2.list_field
