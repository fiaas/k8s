#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_9.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class ScaleStatus(Model):
    """
    ScaleStatus represents the current status of a scale subresource.
    """

    replicas = RequiredField(int)
    selector = Field(six.text_type)


class ScaleSpec(Model):
    """
    ScaleSpec describes the attributes of a scale subresource.
    """

    replicas = Field(int)


class Scale(Model):
    """
    Scale represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "autoscaling/v1")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = ReadOnlyField(ScaleStatus)


class HorizontalPodAutoscalerStatus(Model):
    """
    current status of a horizontal pod autoscaler
    """

    currentCPUUtilizationPercentage = Field(int)
    currentReplicas = RequiredField(int)
    desiredReplicas = RequiredField(int)
    lastScaleTime = Field(datetime.datetime)
    observedGeneration = Field(int)


class CrossVersionObjectReference(Model):
    """
    CrossVersionObjectReference contains enough information to let you identify the
    referred resource.
    """

    name = RequiredField(six.text_type)


class HorizontalPodAutoscalerSpec(Model):
    """
    specification of a horizontal pod autoscaler.
    """

    maxReplicas = RequiredField(int)
    minReplicas = Field(int)
    scaleTargetRef = RequiredField(CrossVersionObjectReference)
    targetCPUUtilizationPercentage = Field(int)


class HorizontalPodAutoscaler(Model):
    """
    configuration of a horizontal pod autoscaler.
    """

    class Meta:
        create_url = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers"
        delete_url = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        get_url = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        list_all_url = "/apis/autoscaling/v1/horizontalpodautoscalers"
        list_ns_url = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers"
        update_url = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watch_url = "/apis/autoscaling/v1/watch/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watchlist_all_url = "/apis/autoscaling/v1/watch/horizontalpodautoscalers"
        watchlist_ns_url = "/apis/autoscaling/v1/watch/namespaces/{namespace}/horizontalpodautoscalers"

    apiVersion = Field(six.text_type, "autoscaling/v1")
    kind = Field(six.text_type, "HorizontalPodAutoscaler")

    metadata = Field(ObjectMeta)
    spec = Field(HorizontalPodAutoscalerSpec)
    status = Field(HorizontalPodAutoscalerStatus)


class HorizontalPodAutoscalerList(Model):
    """
    list of horizontal pod autoscaler objects.
    """
    apiVersion = Field(six.text_type, "autoscaling/v1")
    kind = Field(six.text_type, "HorizontalPodAutoscalerList")

    items = ListField(HorizontalPodAutoscaler)
    metadata = Field(ListMeta)
