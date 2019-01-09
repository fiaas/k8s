#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class JSON(Model):
    """
    JSON represents any valid JSON value. These types are supported: bool, int64,
    float64, string, []interface{}, map[string]interface{} and nil.
    """

    Raw = RequiredField(six.text_type)


class ExternalDocumentation(Model):
    """
    ExternalDocumentation allows referencing an external resource for extended
    documentation.
    """

    description = Field(six.text_type)
    url = Field(six.text_type)


class CustomResourceDefinitionNames(Model):
    """
    CustomResourceDefinitionNames indicates the names to serve this
    CustomResourceDefinition
    """

    listKind = Field(six.text_type)
    plural = RequiredField(six.text_type)
    shortNames = ListField(six.text_type)
    singular = Field(six.text_type)


class CustomResourceDefinitionCondition(Model):
    """
    CustomResourceDefinitionCondition contains details for the current condition of
    this pod.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class CustomResourceDefinitionStatus(Model):
    """
    CustomResourceDefinitionStatus indicates the state of the
    CustomResourceDefinition
    """

    acceptedNames = RequiredField(CustomResourceDefinitionNames)
    conditions = ListField(CustomResourceDefinitionCondition)

