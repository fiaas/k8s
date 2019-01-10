#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

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


class PriorityClass(Model):
    """
    PriorityClass defines mapping from a priority class name to the priority
    integer value. The value can be any valid integer.
    """

    class Meta:
        create_url = "/apis/scheduling.k8s.io/v1alpha1/priorityclasses"
        delete_url = "/apis/scheduling.k8s.io/v1alpha1/priorityclasses/{name}"
        get_url = "/apis/scheduling.k8s.io/v1alpha1/priorityclasses/{name}"
        list_all_url = "/apis/scheduling.k8s.io/v1alpha1/priorityclasses"
        update_url = "/apis/scheduling.k8s.io/v1alpha1/priorityclasses/{name}"
        watch_url = "/apis/scheduling.k8s.io/v1alpha1/watch/priorityclasses/{name}"
        watchlist_all_url = "/apis/scheduling.k8s.io/v1alpha1/watch/priorityclasses"

    apiVersion = Field(six.text_type, "scheduling.k8s.io/v1alpha1")
    kind = Field(six.text_type, "PriorityClass")

    description = Field(six.text_type)
    globalDefault = Field(bool)
    metadata = Field(ObjectMeta)
    value = RequiredField(int)


class PriorityClassList(Model):
    """
    PriorityClassList is a collection of priority classes.
    """
    apiVersion = Field(six.text_type, "scheduling.k8s.io/v1alpha1")
    kind = Field(six.text_type, "PriorityClassList")

    items = ListField(PriorityClass)
    metadata = Field(ListMeta)
