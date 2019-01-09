#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


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


class AdmissionHookClientConfig(Model):
    """
    AdmissionHookClientConfig contains the information to make a TLS connection
    with the webhook
    """

    caBundle = RequiredField(six.text_type)
    service = RequiredField(ServiceReference)


class RuleWithOperations(Model):
    """
    RuleWithOperations is a tuple of Operations and Resources. It is recommended to
    make sure that all the tuple expansions are valid.
    """

    apiGroups = ListField(six.text_type)
    apiVersions = ListField(six.text_type)
    operations = ListField(six.text_type)
    resources = ListField(six.text_type)


class ExternalAdmissionHook(Model):
    """
    ExternalAdmissionHook describes an external admission webhook and the resources
    and operations it applies to.
    """

    clientConfig = RequiredField(AdmissionHookClientConfig)
    failurePolicy = Field(six.text_type)
    name = RequiredField(six.text_type)
    rules = ListField(RuleWithOperations)


class ExternalAdmissionHookConfiguration(Model):
    """
    ExternalAdmissionHookConfiguration describes the configuration of initializers.
    """
    class Meta:
        create_url = "/apis/admissionregistration.k8s.io/v1alpha1/externaladmissionhookconfigurations"
        delete_url = "/apis/admissionregistration.k8s.io/v1alpha1/externaladmissionhookconfigurations/{name}"
        get_url = "/apis/admissionregistration.k8s.io/v1alpha1/externaladmissionhookconfigurations/{name}"
        list_all_url = "/apis/admissionregistration.k8s.io/v1alpha1/externaladmissionhookconfigurations"
        update_url = "/apis/admissionregistration.k8s.io/v1alpha1/externaladmissionhookconfigurations/{name}"
        watch_url = "/apis/admissionregistration.k8s.io/v1alpha1/watch/externaladmissionhookconfigurations/{name}"
        watchlist_all_url = "/apis/admissionregistration.k8s.io/v1alpha1/watch/externaladmissionhookconfigurations"
    
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "ExternalAdmissionHookConfiguration")

    externalAdmissionHooks = ListField(ExternalAdmissionHook)
    metadata = Field(ObjectMeta)


class ExternalAdmissionHookConfigurationList(Model):
    """
    ExternalAdmissionHookConfigurationList is a list of
    ExternalAdmissionHookConfiguration.
    """
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "ExternalAdmissionHookConfigurationList")

    items = ListField(ExternalAdmissionHookConfiguration)
    metadata = Field(ListMeta)


class Rule(Model):
    """
    Rule is a tuple of APIGroups, APIVersion, and Resources.It is recommended to
    make sure that all the tuple expansions are valid.
    """

    apiGroups = ListField(six.text_type)
    apiVersions = ListField(six.text_type)
    resources = ListField(six.text_type)


class Initializer(Model):
    """
    Initializer describes the name and the failure policy of an initializer, and
    what resources it applies to.
    """

    failurePolicy = Field(six.text_type)
    name = RequiredField(six.text_type)
    rules = ListField(Rule)


class InitializerConfiguration(Model):
    """
    InitializerConfiguration describes the configuration of initializers.
    """
    class Meta:
        create_url = "/apis/admissionregistration.k8s.io/v1alpha1/initializerconfigurations"
        delete_url = "/apis/admissionregistration.k8s.io/v1alpha1/initializerconfigurations/{name}"
        get_url = "/apis/admissionregistration.k8s.io/v1alpha1/initializerconfigurations/{name}"
        list_all_url = "/apis/admissionregistration.k8s.io/v1alpha1/initializerconfigurations"
        update_url = "/apis/admissionregistration.k8s.io/v1alpha1/initializerconfigurations/{name}"
        watch_url = "/apis/admissionregistration.k8s.io/v1alpha1/watch/initializerconfigurations/{name}"
        watchlist_all_url = "/apis/admissionregistration.k8s.io/v1alpha1/watch/initializerconfigurations"
    
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "InitializerConfiguration")

    initializers = ListField(Initializer)
    metadata = Field(ObjectMeta)


class InitializerConfigurationList(Model):
    """
    InitializerConfigurationList is a list of InitializerConfiguration.
    """
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "InitializerConfigurationList")

    items = ListField(InitializerConfiguration)
    metadata = Field(ListMeta)

