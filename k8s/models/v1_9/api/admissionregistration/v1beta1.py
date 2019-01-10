#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_9.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta


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
    webhook
    """

    caBundle = RequiredField(six.text_type)
    service = Field(ServiceReference)
    url = Field(six.text_type)


class RuleWithOperations(Model):
    """
    RuleWithOperations is a tuple of Operations and Resources. It is recommended to
    make sure that all the tuple expansions are valid.
    """

    apiGroups = ListField(six.text_type)
    apiVersions = ListField(six.text_type)
    operations = ListField(six.text_type)
    resources = ListField(six.text_type)


class Webhook(Model):
    """
    Webhook describes an admission webhook and the resources and operations it
    applies to.
    """

    clientConfig = RequiredField(WebhookClientConfig)
    failurePolicy = Field(six.text_type)
    name = RequiredField(six.text_type)
    namespaceSelector = Field(LabelSelector)
    rules = ListField(RuleWithOperations)


class ValidatingWebhookConfiguration(Model):
    """
    ValidatingWebhookConfiguration describes the configuration of and admission
    webhook that accept or reject and object without changing it.
    """
    class Meta:
        create_url = "/apis/admissionregistration.k8s.io/v1beta1/validatingwebhookconfigurations"
        delete_url = "/apis/admissionregistration.k8s.io/v1beta1/validatingwebhookconfigurations/{name}"
        get_url = "/apis/admissionregistration.k8s.io/v1beta1/validatingwebhookconfigurations/{name}"
        list_all_url = "/apis/admissionregistration.k8s.io/v1beta1/validatingwebhookconfigurations"
        update_url = "/apis/admissionregistration.k8s.io/v1beta1/validatingwebhookconfigurations/{name}"
        watch_url = "/apis/admissionregistration.k8s.io/v1beta1/watch/validatingwebhookconfigurations/{name}"
        watchlist_all_url = "/apis/admissionregistration.k8s.io/v1beta1/watch/validatingwebhookconfigurations"
    
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "ValidatingWebhookConfiguration")

    metadata = Field(ObjectMeta)
    webhooks = ListField(Webhook)


class ValidatingWebhookConfigurationList(Model):
    """
    ValidatingWebhookConfigurationList is a list of ValidatingWebhookConfiguration.
    """
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "ValidatingWebhookConfigurationList")

    items = ListField(ValidatingWebhookConfiguration)
    metadata = Field(ListMeta)


class MutatingWebhookConfiguration(Model):
    """
    MutatingWebhookConfiguration describes the configuration of and admission
    webhook that accept or reject and may change the object.
    """
    class Meta:
        create_url = "/apis/admissionregistration.k8s.io/v1beta1/mutatingwebhookconfigurations"
        delete_url = "/apis/admissionregistration.k8s.io/v1beta1/mutatingwebhookconfigurations/{name}"
        get_url = "/apis/admissionregistration.k8s.io/v1beta1/mutatingwebhookconfigurations/{name}"
        list_all_url = "/apis/admissionregistration.k8s.io/v1beta1/mutatingwebhookconfigurations"
        update_url = "/apis/admissionregistration.k8s.io/v1beta1/mutatingwebhookconfigurations/{name}"
        watch_url = "/apis/admissionregistration.k8s.io/v1beta1/watch/mutatingwebhookconfigurations/{name}"
        watchlist_all_url = "/apis/admissionregistration.k8s.io/v1beta1/watch/mutatingwebhookconfigurations"
    
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "MutatingWebhookConfiguration")

    metadata = Field(ObjectMeta)
    webhooks = ListField(Webhook)


class MutatingWebhookConfigurationList(Model):
    """
    MutatingWebhookConfigurationList is a list of MutatingWebhookConfiguration.
    """
    apiVersion = Field(six.text_type, "admissionregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "MutatingWebhookConfigurationList")

    items = ListField(MutatingWebhookConfiguration)
    metadata = Field(ListMeta)

