#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_13.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class LeaseSpec(Model):
    """
    LeaseSpec is a specification of a Lease.
    """

    acquireTime = Field(datetime.datetime)
    holderIdentity = Field(six.text_type)
    leaseDurationSeconds = Field(int)
    leaseTransitions = Field(int)
    renewTime = Field(datetime.datetime)


class Lease(Model):
    """
    Lease defines a lease concept.
    """
    class Meta:
        create_url = "/apis/coordination.k8s.io/v1beta1/namespaces/{namespace}/leases"
        delete_url = "/apis/coordination.k8s.io/v1beta1/namespaces/{namespace}/leases/{name}"
        get_url = "/apis/coordination.k8s.io/v1beta1/namespaces/{namespace}/leases/{name}"
        list_all_url = "/apis/coordination.k8s.io/v1beta1/leases"
        list_ns_url = "/apis/coordination.k8s.io/v1beta1/namespaces/{namespace}/leases"
        update_url = "/apis/coordination.k8s.io/v1beta1/namespaces/{namespace}/leases/{name}"
        watch_url = "/apis/coordination.k8s.io/v1beta1/watch/namespaces/{namespace}/leases/{name}"
        watchlist_all_url = "/apis/coordination.k8s.io/v1beta1/watch/leases"
        watchlist_ns_url = "/apis/coordination.k8s.io/v1beta1/watch/namespaces/{namespace}/leases"
    
    apiVersion = Field(six.text_type, "coordination.k8s.io/v1beta1")
    kind = Field(six.text_type, "Lease")

    metadata = Field(ObjectMeta)
    spec = Field(LeaseSpec)


class LeaseList(Model):
    """
    LeaseList is a list of Lease objects.
    """
    apiVersion = Field(six.text_type, "coordination.k8s.io/v1beta1")
    kind = Field(six.text_type, "LeaseList")

    items = ListField(Lease)
    metadata = Field(ListMeta)

