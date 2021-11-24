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

from __future__ import absolute_import

import datetime

import six

from .common import ObjectMeta
from .apiextensions_v1 import JSONSchemaProps, WebhookConversion
from ..base import Model
from ..fields import Field, ListField


class CustomResourceColumnDefinition(Model):
    description = Field(six.text_type)
    format = Field(six.text_type)
    jsonPath = Field(six.text_type)
    name = Field(six.text_type)
    priority = Field(int)
    type = Field(six.text_type)


class CustomResourceConversion(Model):
    strategy = Field(six.text_type)
    webhook = Field(WebhookConversion)


class CustomResourceDefinitionNames(Model):
    categories = ListField(six.text_type)
    kind = Field(six.text_type)
    listKind = Field(six.text_type)
    plural = Field(six.text_type)
    shortNames = ListField(six.text_type)
    singular = Field(six.text_type)


class CustomResourceValidation(Model):
    # This field is fully defined in the API Reference, but in essence it is simply a JSON-schema
    # following Specification Draft 4 (http://json-schema.org/)
    # TODO specify full schema
    openAPIV3Schema = Field(JSONSchemaProps)


class CustomResourceSubresourceScale(Model):
    labelSelectorPath = Field(six.text_type)
    specReplicasPath = Field(six.text_type)
    statusReplicasPath = Field(six.text_type)


class CustomResourceSubresources(Model):
    scale = Field(CustomResourceSubresourceScale)
    # CustomResourceSubresourceStatus contains no fields,
    # so we use the dict type instead
    status = Field(dict)


class CustomResourceDefinitionVersion(Model):
    additionalPrinterColumns = ListField(CustomResourceColumnDefinition)
    deprecated = Field(bool)
    deprecationWarning = Field(six.text_type)
    name = Field(six.text_type)
    schema = Field(CustomResourceValidation)
    served = Field(bool)
    storage = Field(bool)
    subresources = Field(CustomResourceSubresources)


class CustomResourceDefinitionSpec(Model):
    conversion = Field(CustomResourceConversion)
    group = Field(six.text_type)
    names = Field(CustomResourceDefinitionNames)
    scope = Field(six.text_type)
    validation = Field(CustomResourceValidation)
    versions = ListField(CustomResourceDefinitionVersion)


class CustomResourceDefinitionCondition(Model):
    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = Field(six.text_type)
    type = Field(six.text_type)


class CustomResourceDefinitionStatus(Model):
    acceptedNames = Field(CustomResourceDefinitionNames)
    conditions = ListField(CustomResourceDefinitionCondition)
    storedVersions = ListField(six.text_type)


class CustomResourceDefinition(Model):
    class Meta:
        url_template = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}"
        list_url = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions"
        watch_list_url = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions?watch=true"

    metadata = Field(ObjectMeta)
    spec = Field(CustomResourceDefinitionSpec)
    status = Field(CustomResourceDefinitionStatus)
