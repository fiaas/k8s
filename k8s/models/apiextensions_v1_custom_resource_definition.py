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
from ..base import Model, SelfModel
from ..fields import Field, ListField, JSONField


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
    default = JSONField()
    definitions = Field(dict)
    dependencies = Field(dict)
    description = Field(six.text_type)
    enum = JSONField()
    example = JSONField()
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
    _not = Field(SelfModel)
    nullable = Field(bool)
    oneOf = ListField(SelfModel)
    pattern = Field(six.text_type)
    patternProperties = Field(dict)
    properties = Field(dict)
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
    preserveUnknownFields = Field(bool)
    scope = Field(six.text_type)
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
