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

# pylint: disable=R0201

from datetime import datetime

import pytest
import pytz
import six
import mock

from k8s import config
from k8s.base import Model, SelfModel
from k8s.fields import Field, JSONField, ListField, OnceField, ReadOnlyField, RequiredField
from k8s.models.common import ObjectMeta

NAME = "my-model-test"


class ModelTest(Model):
    class Meta:
        url_template = "/apis/v1/modeltests/{name}"

    metadata = Field(ObjectMeta)
    field = Field(int)
    list_field = ListField(int)
    once_field = OnceField(int)
    read_only_field = ReadOnlyField(int)
    alt_type_field = Field(int, alt_type=six.text_type)
    dict_field = Field(dict)
    _exec = Field(int)
    time_field = Field(datetime)
    json_field = JSONField()
    self_field = Field(SelfModel)


class TestFields(object):
    @pytest.fixture(autouse=True)
    def set_config_debug(self, monkeypatch):
        monkeypatch.setattr(config, "debug", True)

    @pytest.mark.parametrize("field_name,initial_value,other_value", (
        ("field", 1, 2),
        ("list_field", [1], [1, 2]),
        ("once_field", 1, 2),
        ("_exec", 1, 2),
        ("json_field", 1, [1, 2]),
    ))
    def test_field_new(self, field_name, initial_value, other_value):
        kwargs = {"new": True, field_name: initial_value}
        model = ModelTest(**kwargs)
        assert getattr(model, field_name) == initial_value
        setattr(model, field_name, other_value)
        assert getattr(model, field_name) == other_value

    @pytest.mark.parametrize("field_name,initial_value,other_value", (
        ("field", 1, 2),
        ("list_field", [1], [1, 2]),
    ))
    def test_field_old(self, field_name, initial_value, other_value):
        model = ModelTest.from_dict({field_name: initial_value})
        assert getattr(model, field_name) == initial_value
        setattr(model, field_name, other_value)
        assert getattr(model, field_name) == other_value

    def test_once_field_old(self):
        model = ModelTest.from_dict({"once_field": 1})
        assert model.once_field == 1
        model.once_field = 2
        assert model.once_field == 1

    def test_exec_field_old(self):
        model = ModelTest.from_dict({"exec": 1})
        assert model._exec == 1
        model._exec = 2
        assert model._exec == 2
        assert model.as_dict()[u"exec"] == 2

    def test_read_only_field_new(self):
        model = ModelTest(new=True, read_only_field=1)
        assert model.read_only_field is None
        model.read_only_field = 2
        assert model.read_only_field is None

    def test_read_only_field_old(self):
        model = ModelTest.from_dict({"read_only_field": 1})
        assert model.read_only_field == 1
        model.read_only_field = 2
        assert model.read_only_field == 1

    @pytest.mark.parametrize("value,modifier", [
        (1, lambda x: x + 1),
        (u"string", lambda x: x.upper())
    ])
    def test_alt_type_field(self, value, modifier):
        model = ModelTest.from_dict({"alt_type_field": value})
        assert model.alt_type_field == value
        assert model.as_dict()[u"alt_type_field"] == value
        model.alt_type_field = modifier(value)
        assert model.alt_type_field == modifier(value)

    @pytest.mark.parametrize("input,dt", (
        ("2009-01-01T17:59:59Z", datetime(2009, 1, 1, 17, 59, 59, tzinfo=pytz.UTC)),
        ("2009-01-01T17:59:59+01:00", datetime(2009, 1, 1, 16, 59, 59, tzinfo=pytz.UTC)),
    ))
    def test_time_field_from_dict(self, input, dt):
        model = ModelTest.from_dict({"time_field": input})
        assert isinstance(model.time_field, datetime)
        assert model.time_field == dt

    def test_time_field_as_dict(self):
        model = ModelTest(time_field=datetime(2009, 1, 1, 17, 59, 59, tzinfo=pytz.UTC))
        d = model.as_dict()
        assert d["time_field"] == "2009-01-01T17:59:59Z"

    @pytest.mark.parametrize("value,is_valid", (
        (None, True),
        (1, True),
        (1.1, True),
        ("string", True),
        ([1, 2], True),
        ({"key": "value"}, True),
        (ModelTest(), False),
        ([1, None], False),
    ))
    def test_json_field_validation(self, value, is_valid):
        model = ModelTest()
        if is_valid:
            setattr(model, "json_field", value)
            assert model.json_field == value
        else:
            with pytest.raises(TypeError):
                setattr(model, "json_field", value)
            assert model.json_field is None


class RequiredFieldTest(Model):
    required_field = RequiredField(int)
    field = Field(int, 100)


@pytest.mark.usefixtures("logger")
class TestRequiredField(object):
    @pytest.mark.parametrize("kwargs", [
        {"required_field": 1, "field": 2},
        {"required_field": 1},
    ])
    def test_create_with_fields(self, kwargs):
        instance = RequiredFieldTest(new=True, **kwargs)
        for key, value in kwargs.items():
            assert getattr(instance, key) == value

    def test_create_fails_when_field_missing(self):
        with pytest.raises(TypeError):
            RequiredFieldTest(new=True, field=1)


class TestSelfField(object):
    def test_create_from_dict(self):
        model = ModelTest.from_dict({"self_field": {"exec": 1}})
        assert getattr(model, "self_field") == ModelTest(_exec=1)

    def test_get_or_create_merge(self, get):
        get.return_value = _create_mock_response()
        object_meta = ObjectMeta(name=NAME, labels={"test": "true"})
        model = ModelTest.get_or_create(metadata=object_meta, self_field=ModelTest(_exec=1))
        assert getattr(model, "self_field") == ModelTest.from_dict({"read_only_field": 1, "exec": 1})


def _create_mock_response():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "apiVersion": "v1",
        "kind": "ModelTest",
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
        "self_field": {
            "read_only_field": 1
        }
    }
    return mock_response


def _uri(name=""):
    return "/apis/v1/modeltests/{name}".format(name=name)
