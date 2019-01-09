#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


class APIServiceCondition(Model):
    """
    
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = Field(six.text_type)
    type = Field(six.text_type)


class APIServiceStatus(Model):
    """
    APIServiceStatus contains derived information about an API server
    """

    conditions = ListField(APIServiceCondition)


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

    caBundle = Field(six.text_type)
    group = Field(six.text_type)
    groupPriorityMinimum = Field(int)
    insecureSkipTLSVerify = Field(bool)
    service = Field(ServiceReference)
    version = Field(six.text_type)
    versionPriority = Field(int)


class APIService(Model):
    """
    APIService represents a server for a particular GroupVersion. Name must be
    'version.group'.
    """

    metadata = Field(ObjectMeta)
    spec = Field(APIServiceSpec)
    status = Field(APIServiceStatus)


class APIServiceList(Model):
    """
    APIServiceList is a list of APIService objects.
    """

    items = ListField(APIService)
    metadata = Field(ListMeta)

