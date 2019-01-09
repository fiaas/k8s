#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import DeleteOptions, LabelSelector, ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class PodDisruptionBudgetStatus(Model):
    """
    PodDisruptionBudgetStatus represents information about the status of a
    PodDisruptionBudget. Status may trail the actual state of a system.
    """

    currentHealthy = RequiredField(int)
    desiredHealthy = RequiredField(int)
    disruptedPods = RequiredField(dict)
    disruptionsAllowed = RequiredField(int)
    expectedPods = RequiredField(int)
    observedGeneration = Field(int)


class PodDisruptionBudgetSpec(Model):
    """
    PodDisruptionBudgetSpec is a description of a PodDisruptionBudget.
    """

    minAvailable = Field(six.text_type, alt_type=int)
    selector = Field(LabelSelector)


class PodDisruptionBudget(Model):
    """
    PodDisruptionBudget is an object to define the max disruption that can be
    caused to a collection of pods
    """
    class Meta:
        create_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets"
        delete_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        get_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        list_all_url = "/apis/policy/v1beta1/poddisruptionbudgets"
        list_ns_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets"
        update_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        watch_url = "/apis/policy/v1beta1/watch/namespaces/{namespace}/poddisruptionbudgets/{name}"
        watchlist_all_url = "/apis/policy/v1beta1/watch/poddisruptionbudgets"
        watchlist_ns_url = "/apis/policy/v1beta1/watch/namespaces/{namespace}/poddisruptionbudgets"
    
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodDisruptionBudget")

    metadata = Field(ObjectMeta)
    spec = Field(PodDisruptionBudgetSpec)
    status = Field(PodDisruptionBudgetStatus)


class PodDisruptionBudgetList(Model):
    """
    PodDisruptionBudgetList is a collection of PodDisruptionBudgets.
    """
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodDisruptionBudgetList")

    items = ListField(PodDisruptionBudget)
    metadata = Field(ListMeta)


class Eviction(Model):
    """
    Eviction evicts a pod from its node subject to certain policies and safety
    constraints. This is a subresource of Pod.  A request to cause such an eviction
    is created by POSTing to .../pods/<pod name>/evictions.
    """
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "Eviction")

    deleteOptions = Field(DeleteOptions)
    metadata = Field(ObjectMeta)

