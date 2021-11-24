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

import six

from ..base import Model, SelfModel
from ..fields import Field, ListField, AnyField


class ExternalDocumentation(Model):
    description = Field(six.text_type)
    url = Field(six.text_type)


class JSONSchemaProps(Model):
    ref = Field(six.text_type, name='$ref')
    schema = Field(six.text_type, name='$schema')
    additionalItems = Field(SelfModel, alt_type=bool)
    additionalProperties = Field(SelfModel, alt_type=bool)
    allOf = ListField(SelfModel)
    anyOf = ListField(SelfModel)
    default = AnyField()
    definitions = Field(object)
    dependencies = Field(object)
    description = Field(six.text_type)
    enum = AnyField()
    example = AnyField()
    exclusiveMaximum = Field(bool)
    exclusiveMinimum = Field(bool)
    externalDocs = Field(ExternalDocumentation)
    format = Field(six.text_type)
    id = Field(six.text_type)
    items = Field(SelfModel, alt_type=list)
    maxItems = Field(int)
    maxLength = Field(int)
    maxProperties = Field(int)
    maximum = Field(int, alt_type=float)
    minItems = Field(int)
    minLength = Field(int)
    minProperties = Field(int)
    minimum = Field(int, alt_type=float)
    multipleOf = Field(int, alt_type=float)
    not_ = Field(SelfModel, name='not')
    nullable = Field(bool)
    oneOf = ListField(SelfModel)
    pattern = Field(six.text_type)
    patternProperties = Field(object)
    properties = Field(object)
    required = ListField(six.text_type)
    title = Field(six.text_type)
    type = Field(six.text_type)
    uniqueItems = Field(bool)
    x_kubernetes_embedded_resource = Field(bool, name='x-kubernetes-embedded-resource')
    x_kubernetes_int_or_string = Field(bool, name='x-kubernetes-int-or-string')
    x_kubernetes_list_map_keys = ListField(six.text_type, name='x-kubernetes-list-map-keys')
    x_kubernetes_list_type = Field(six.text_type, name="x-kubernetes-list-type")
    x_kubernetes_map_type = Field(six.text_type, name='x-kubernetes-map-type')
    x_kubernetes_preserve_unknown_fields = Field(bool, name="x-kubernetes-preserve-unknown-fields")


class ServiceReference(Model):
    name = Field(six.text_type)
    namespace = Field(six.text_type)
    path = Field(six.text_type)
    port = Field(int)


class WebhookClientConfig(Model):
    caBundle = Field(six.text_type)
    service = Field(ServiceReference)
    url = Field(six.text_type)


class WebhookConversion(Model):
    clientConfig = Field(WebhookClientConfig)
    conversionReviewVersions = ListField(six.text_type)
