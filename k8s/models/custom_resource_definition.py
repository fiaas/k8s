#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class CustomResourceDefinitionNames(Model):
    kind = Field(six.text_type)
    listKind = Field(six.text_type)
    plural = Field(six.text_type)
    shortNames = ListField(six.text_type)
    singular = Field(six.text_type)


class CustomResourceValidation(Model):
    # This field is fully defined in the API Reference, but in essence it is simply a JSON-schema
    # following Specification Draft 4 (http://json-schema.org/)
    openAPIV3Schema = Field(dict)


class CustomResourceDefinitionSpec(Model):
    group = Field(six.text_type)
    names = Field(CustomResourceDefinitionNames)
    scope = Field(six.text_type)
    validation = Field(CustomResourceValidation)
    version = Field(six.text_type)


class CustomResourceDefinitionCondition(Model):
    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = Field(six.text_type)
    type = Field(six.text_type)


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
