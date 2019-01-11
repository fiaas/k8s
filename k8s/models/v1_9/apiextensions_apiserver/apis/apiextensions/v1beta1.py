#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_9.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class ExternalDocumentation(Model):
    """
    ExternalDocumentation allows referencing an external resource for extended
    documentation.
    """

    description = Field(six.text_type)
    url = Field(six.text_type)


class CustomResourceValidation(Model):
    """
    CustomResourceValidation is a list of validation methods for CustomResources.
    """

    openAPIV3Schema = Field(dict)


class CustomResourceDefinitionNames(Model):
    """
    CustomResourceDefinitionNames indicates the names to serve this
    CustomResourceDefinition
    """

    kind = RequiredField(six.text_type)
    listKind = Field(six.text_type)
    plural = RequiredField(six.text_type)
    shortNames = ListField(six.text_type)
    singular = Field(six.text_type)


class CustomResourceDefinitionSpec(Model):
    """
    CustomResourceDefinitionSpec describes how a user wants their resource to
    appear
    """

    group = RequiredField(six.text_type)
    names = RequiredField(CustomResourceDefinitionNames)
    scope = RequiredField(six.text_type)
    validation = Field(CustomResourceValidation)
    version = RequiredField(six.text_type)


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


class CustomResourceDefinition(Model):
    """
    CustomResourceDefinition represents a resource that should be exposed on the
    API server.  Its name MUST be in the format <.spec.name>.<.spec.group>.
    """

    class Meta:
        create_url = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions"
        delete_url = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions/{name}"
        get_url = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions/{name}"
        list_all_url = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions"
        update_url = "/apis/apiextensions.k8s.io/v1beta1/customresourcedefinitions/{name}"
        watch_url = "/apis/apiextensions.k8s.io/v1beta1/watch/customresourcedefinitions/{name}"
        watchlist_all_url = "/apis/apiextensions.k8s.io/v1beta1/watch/customresourcedefinitions"

    apiVersion = Field(six.text_type, "apiextensions.k8s.io/v1beta1")
    kind = Field(six.text_type, "CustomResourceDefinition")

    metadata = Field(ObjectMeta)
    spec = Field(CustomResourceDefinitionSpec)
    status = Field(CustomResourceDefinitionStatus)


class CustomResourceDefinitionList(Model):
    """
    CustomResourceDefinitionList is a list of CustomResourceDefinition objects.
    """
    apiVersion = Field(six.text_type, "apiextensions.k8s.io/v1beta1")
    kind = Field(six.text_type, "CustomResourceDefinitionList")

    items = ListField(CustomResourceDefinition)
    metadata = Field(ListMeta)
