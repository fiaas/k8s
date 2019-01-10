#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_11.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


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

