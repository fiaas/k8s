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


class ServiceReference(Model):
    """
    ServiceReference holds a reference to Service.legacy.k8s.io
    """

    name = Field(six.text_type)
    namespace = Field(six.text_type)


class APIServiceSpec(Model):
    """
    APIServiceSpec contains information for locating and communicating with a
    server. Only https is supported, though you are able to disable certificate
    verification.
    """

    caBundle = RequiredField(six.text_type)
    group = Field(six.text_type)
    groupPriorityMinimum = RequiredField(int)
    insecureSkipTLSVerify = Field(bool)
    service = RequiredField(ServiceReference)
    version = Field(six.text_type)
    versionPriority = RequiredField(int)


class APIServiceCondition(Model):
    """
    
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class APIServiceStatus(Model):
    """
    APIServiceStatus contains derived information about an API server
    """

    conditions = ListField(APIServiceCondition)


class APIService(Model):
    """
    APIService represents a server for a particular GroupVersion. Name must be
    'version.group'.
    """

    class Meta:
        create_url = "/apis/apiregistration.k8s.io/v1beta1/apiservices"
        delete_url = "/apis/apiregistration.k8s.io/v1beta1/apiservices/{name}"
        get_url = "/apis/apiregistration.k8s.io/v1beta1/apiservices/{name}"
        list_all_url = "/apis/apiregistration.k8s.io/v1beta1/apiservices"
        update_url = "/apis/apiregistration.k8s.io/v1beta1/apiservices/{name}"
        watch_url = "/apis/apiregistration.k8s.io/v1beta1/watch/apiservices/{name}"
        watchlist_all_url = "/apis/apiregistration.k8s.io/v1beta1/watch/apiservices"

    apiVersion = Field(six.text_type, "apiregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "APIService")

    metadata = Field(ObjectMeta)
    spec = Field(APIServiceSpec)
    status = Field(APIServiceStatus)


class APIServiceList(Model):
    """
    APIServiceList is a list of APIService objects.
    """
    apiVersion = Field(six.text_type, "apiregistration.k8s.io/v1beta1")
    kind = Field(six.text_type, "APIServiceList")

    items = ListField(APIService)
    metadata = Field(ListMeta)
