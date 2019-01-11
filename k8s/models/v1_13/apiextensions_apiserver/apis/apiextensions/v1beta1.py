#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_13.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class ServiceReference(Model):
    """
    ServiceReference holds a reference to Service.legacy.k8s.io
    """

    name = RequiredField(six.text_type)
    namespace = RequiredField(six.text_type)
    path = Field(six.text_type)


class WebhookClientConfig(Model):
    """
    WebhookClientConfig contains the information to make a TLS connection with the
    webhook. It has the same field as
    admissionregistration.v1beta1.WebhookClientConfig.
    """

    caBundle = Field(six.text_type)
    service = Field(ServiceReference)
    url = Field(six.text_type)


class CustomResourceConversion(Model):
    """
    CustomResourceConversion describes how to convert different versions of a CR.
    """

    strategy = RequiredField(six.text_type)
    webhookClientConfig = Field(WebhookClientConfig)


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


class CustomResourceSubresourceScale(Model):
    """
    CustomResourceSubresourceScale defines how to serve the scale subresource for
    CustomResources.
    """

    labelSelectorPath = Field(six.text_type)
    specReplicasPath = RequiredField(six.text_type)
    statusReplicasPath = RequiredField(six.text_type)


class CustomResourceSubresources(Model):
    """
    CustomResourceSubresources defines the status and scale subresources for
    CustomResources.
    """

    scale = Field(CustomResourceSubresourceScale)
    status = Field(dict)


class CustomResourceDefinitionNames(Model):
    """
    CustomResourceDefinitionNames indicates the names to serve this
    CustomResourceDefinition
    """

    categories = ListField(six.text_type)
    kind = RequiredField(six.text_type)
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
    storedVersions = ListField(six.text_type)


class CustomResourceColumnDefinition(Model):
    """
    CustomResourceColumnDefinition specifies a column for server side printing.
    """

    JSONPath = RequiredField(six.text_type)
    description = Field(six.text_type)
    format = Field(six.text_type)
    name = RequiredField(six.text_type)
    priority = Field(int)
    type = RequiredField(six.text_type)


class CustomResourceDefinitionVersion(Model):
    """
    CustomResourceDefinitionVersion describes a version for CRD.
    """

    additionalPrinterColumns = ListField(CustomResourceColumnDefinition)
    name = RequiredField(six.text_type)
    schema = Field(CustomResourceValidation)
    served = RequiredField(bool)
    storage = RequiredField(bool)
    subresources = Field(CustomResourceSubresources)


class CustomResourceDefinitionSpec(Model):
    """
    CustomResourceDefinitionSpec describes how a user wants their resource to
    appear
    """

    additionalPrinterColumns = ListField(CustomResourceColumnDefinition)
    conversion = Field(CustomResourceConversion)
    group = RequiredField(six.text_type)
    names = RequiredField(CustomResourceDefinitionNames)
    scope = RequiredField(six.text_type)
    subresources = Field(CustomResourceSubresources)
    validation = Field(CustomResourceValidation)
    version = Field(six.text_type)
    versions = ListField(CustomResourceDefinitionVersion)


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
    spec = RequiredField(CustomResourceDefinitionSpec)
    status = Field(CustomResourceDefinitionStatus)


class CustomResourceDefinitionList(Model):
    """
    CustomResourceDefinitionList is a list of CustomResourceDefinition objects.
    """
    apiVersion = Field(six.text_type, "apiextensions.k8s.io/v1beta1")
    kind = Field(six.text_type, "CustomResourceDefinitionList")

    items = ListField(CustomResourceDefinition)
    metadata = Field(ListMeta)
