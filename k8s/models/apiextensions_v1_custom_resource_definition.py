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
from ..base import Model, SelfModel
from ..fields import Field, ListField, JSONField


class ExternalDocumentation(Model):
    description = Field(str)
    url = Field(str)


class JSONSchemaProps(Model):
    ref = Field(str, name='$ref')
    schema = Field(str, name='$schema')
    additionalItems = Field(SelfModel, alt_type=bool)
    additionalProperties = Field(SelfModel, alt_type=bool)
    allOf = ListField(SelfModel)
    anyOf = ListField(SelfModel)
    default = JSONField()
    definitions = Field(dict)
    dependencies = Field(dict)
    description = Field(str)
    enum = JSONField()
    example = JSONField()
    exclusiveMaximum = Field(bool)
    exclusiveMinimum = Field(bool)
    externalDocs = Field(ExternalDocumentation)
    format = Field(str)
    id = Field(str)
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
    pattern = Field(str)
    patternProperties = Field(dict)
    properties = Field(dict)
    required = ListField(str)
    title = Field(str)
    type = Field(str)
    uniqueItems = Field(bool)
    x_kubernetes_embedded_resource = Field(bool, name='x-kubernetes-embedded-resource')
    x_kubernetes_int_or_string = Field(bool, name='x-kubernetes-int-or-string')
    x_kubernetes_list_map_keys = ListField(str, name='x-kubernetes-list-map-keys')
    x_kubernetes_list_type = Field(str, name="x-kubernetes-list-type")
    x_kubernetes_map_type = Field(str, name='x-kubernetes-map-type')
    x_kubernetes_preserve_unknown_fields = Field(bool, name="x-kubernetes-preserve-unknown-fields")


class JSONSchemaPropsStatusEnabled(Model):
    ref = Field(str, name='$ref')
    schema = Field(str, name='$schema')

    description = Field(str)
    example = JSONField()
    exclusiveMaximum = Field(bool)
    exclusiveMinimum = Field(bool)
    externalDocs = Field(ExternalDocumentation)
    format = Field(str)
    items = Field(SelfModel, alt_type=list)
    maxItems = Field(int)
    maxLength = Field(int)
    maximum = Field(int, alt_type=float)
    minItems = Field(int)
    minLength = Field(int)
    minimum = Field(int, alt_type=float)
    multipleOf = Field(int, alt_type=float)
    pattern = Field(str)
    properties = Field(dict)
    required = ListField(str)
    title = Field(str)
    type = Field(str)


class ServiceReference(Model):
    name = Field(str)
    namespace = Field(str)
    path = Field(str)
    port = Field(int)


class WebhookClientConfig(Model):
    caBundle = Field(str)
    service = Field(ServiceReference)
    url = Field(str)


class WebhookConversion(Model):
    clientConfig = Field(WebhookClientConfig)
    conversionReviewVersions = ListField(str)


class CustomResourceColumnDefinition(Model):
    description = Field(str)
    format = Field(str)
    jsonPath = Field(str)
    name = Field(str)
    priority = Field(int)
    type = Field(str)


class CustomResourceConversion(Model):
    strategy = Field(str)
    webhook = Field(WebhookConversion)


class CustomResourceDefinitionNames(Model):
    categories = ListField(str)
    kind = Field(str)
    listKind = Field(str)
    plural = Field(str)
    shortNames = ListField(str)
    singular = Field(str)


class CustomResourceValidation(Model):
    openAPIV3Schema = Field(JSONSchemaProps, alt_type=JSONSchemaPropsStatusEnabled)


class CustomResourceSubresourceScale(Model):
    labelSelectorPath = Field(str)
    specReplicasPath = Field(str)
    statusReplicasPath = Field(str)


class CustomResourceSubresourceStatus(Model):
    pass


class CustomResourceSubresources(Model):
    scale = Field(CustomResourceSubresourceScale)
    status = Field(CustomResourceSubresourceStatus)


class CustomResourceDefinitionVersion(Model):
    additionalPrinterColumns = ListField(CustomResourceColumnDefinition)
    deprecated = Field(bool)
    deprecationWarning = Field(str)
    name = Field(str)
    schema = Field(CustomResourceValidation)
    served = Field(bool)
    storage = Field(bool)
    subresources = Field(CustomResourceSubresources)


class CustomResourceDefinitionSpec(Model):
    conversion = Field(CustomResourceConversion)
    group = Field(str)
    names = Field(CustomResourceDefinitionNames)
    preserveUnknownFields = Field(bool)
    scope = Field(str)
    versions = ListField(CustomResourceDefinitionVersion)


class CustomResourceDefinitionCondition(Model):
    lastTransitionTime = Field(datetime.datetime)
    message = Field(str)
    reason = Field(str)
    status = Field(str)
    type = Field(str)


class CustomResourceDefinitionStatus(Model):
    acceptedNames = Field(CustomResourceDefinitionNames)
    conditions = ListField(CustomResourceDefinitionCondition)
    storedVersions = ListField(str)


class CustomResourceDefinition(Model):
    class Meta:
        url_template = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}"
        list_url = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions"
        watch_list_url = "/apis/apiextensions.k8s.io/v1/customresourcedefinitions?watch=true"

    metadata = Field(ObjectMeta)
    spec = Field(CustomResourceDefinitionSpec)
    status = Field(CustomResourceDefinitionStatus)
