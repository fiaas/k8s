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


import datetime

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class CustomResourceDefinitionNames(Model):
    kind = Field(str)
    listKind = Field(str)
    plural = Field(str)
    shortNames = ListField(str)
    singular = Field(str)


class CustomResourceValidation(Model):
    # This field is fully defined in the API Reference, but in essence it is simply a JSON-schema
    # following Specification Draft 4 (http://json-schema.org/)
    openAPIV3Schema = Field(dict)


class CustomResourceDefinitionSpec(Model):
    group = Field(str)
    names = Field(CustomResourceDefinitionNames)
    scope = Field(str)
    validation = Field(CustomResourceValidation)
    version = Field(str)


class CustomResourceDefinitionCondition(Model):
    lastTransitionTime = Field(datetime.datetime)
    message = Field(str)
    reason = Field(str)
    status = Field(str)
    type = Field(str)


class CustomResourceDefinitionStatus(Model):
    acceptedNames = Field(CustomResourceDefinitionNames)
    conditions = ListField(CustomResourceDefinitionCondition)


class CustomResourceDefinition(Model):
    class Meta:
        url_template = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions/{name}"
        watch_list_url = "/apis/apiextensions.k8s.io/v1beta1/watch/customresourcedefinitions"

    metadata = Field(ObjectMeta)
    spec = Field(CustomResourceDefinitionSpec)
    status = Field(CustomResourceDefinitionStatus)
