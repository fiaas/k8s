#!/usr/bin/env python
# -*- coding: utf-8
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

    def test_set_dict_field_to_none(self, mock_response):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {'dict_field': {'thing': 'otherthing'}}
        instance = ModelTest.get_or_create(metadata=metadata, dict_field=None)
        assert instance.dict_field is None

    def test_annotations_merge(self, mock_response):
        mock_response.json.return_value = {
            u"metadata": {
                u"name": u"my-name",
                u"namespace": u"my-namespace",
                u"annotations": {
                    u"must_keep": u"this",
                    u"will_overwrite": u"this"
                }
            }
        }
        metadata = ObjectMeta(name="my-name", namespace="my-namespace", annotations={u"will_overwrite": u"that"})
        instance = ModelTest.get_or_create(metadata=metadata)
        assert instance.metadata.annotations[u"will_overwrite"] == u"that"
        assert instance.metadata.annotations[u"must_keep"] == u"this"
