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


class ResourceMetricStatus(Model):
    """
    ResourceMetricStatus indicates the current value of a resource metric known to
    Kubernetes, as specified in requests and limits, describing each pod in the
    current scale target (e.g. CPU or memory).  Such metrics are built in to
    Kubernetes, and have special scaling options on top of those available to
    normal per-pod metrics using the 'pods' source.
    """

    currentAverageUtilization = Field(int)
    currentAverageValue = RequiredField(six.text_type)
    name = RequiredField(six.text_type)


class ResourceMetricSource(Model):
    """
    ResourceMetricSource indicates how to scale on a resource metric known to
    Kubernetes, as specified in requests and limits, describing each pod in the
    current scale target (e.g. CPU or memory).  The values will be averaged
    together before being compared to the target.  Such metrics are built in to
    Kubernetes, and have special scaling options on top of those available to
    normal per-pod metrics using the 'pods' source.  Only one 'target' type should
    be set.
    """

    name = RequiredField(six.text_type)
    targetAverageUtilization = Field(int)
    targetAverageValue = Field(six.text_type)


class PodsMetricStatus(Model):
    """
    PodsMetricStatus indicates the current value of a metric describing each pod in
    the current scale target (for example, transactions-processed-per-second).
    """

    currentAverageValue = RequiredField(six.text_type)
    metricName = RequiredField(six.text_type)


class PodsMetricSource(Model):
    """
    PodsMetricSource indicates how to scale on a metric describing each pod in the
    current scale target (for example, transactions-processed-per-second). The
    values will be averaged together before being compared to the target value.
    """

    metricName = RequiredField(six.text_type)
    targetAverageValue = RequiredField(six.text_type)


class HorizontalPodAutoscalerCondition(Model):
    """
    HorizontalPodAutoscalerCondition describes the state of a
    HorizontalPodAutoscaler at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class CrossVersionObjectReference(Model):
    """
    CrossVersionObjectReference contains enough information to let you identify the
    referred resource.
    """

    name = RequiredField(six.text_type)


class ObjectMetricStatus(Model):
    """
    ObjectMetricStatus indicates the current value of a metric describing a
    kubernetes object (for example, hits-per-second on an Ingress object).
    """

    currentValue = RequiredField(six.text_type)
    metricName = RequiredField(six.text_type)
    target = RequiredField(CrossVersionObjectReference)


class MetricStatus(Model):
    """
    MetricStatus describes the last-read state of a single metric.
    """

    object = Field(ObjectMetricStatus)
    pods = Field(PodsMetricStatus)
    resource = Field(ResourceMetricStatus)
    type = RequiredField(six.text_type)


class HorizontalPodAutoscalerStatus(Model):
    """
    HorizontalPodAutoscalerStatus describes the current status of a horizontal pod
    autoscaler.
    """

    conditions = ListField(HorizontalPodAutoscalerCondition)
    currentMetrics = ListField(MetricStatus)
    currentReplicas = RequiredField(int)
    desiredReplicas = RequiredField(int)
    lastScaleTime = Field(datetime.datetime)
    observedGeneration = Field(int)


class ObjectMetricSource(Model):
    """
    ObjectMetricSource indicates how to scale on a metric describing a kubernetes
    object (for example, hits-per-second on an Ingress object).
    """

    metricName = RequiredField(six.text_type)
    target = RequiredField(CrossVersionObjectReference)
    targetValue = RequiredField(six.text_type)


class MetricSpec(Model):
    """
    MetricSpec specifies how to scale based on a single metric (only `type` and one
    other matching field should be set at once).
    """

    object = Field(ObjectMetricSource)
    pods = Field(PodsMetricSource)
    resource = Field(ResourceMetricSource)
    type = RequiredField(six.text_type)


class HorizontalPodAutoscalerSpec(Model):
    """
    HorizontalPodAutoscalerSpec describes the desired functionality of the
    HorizontalPodAutoscaler.
    """

    maxReplicas = RequiredField(int)
    metrics = ListField(MetricSpec)
    minReplicas = Field(int)
    scaleTargetRef = RequiredField(CrossVersionObjectReference)


class HorizontalPodAutoscaler(Model):
    """
    HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler,
    which automatically manages the replica count of any resource implementing the
    scale subresource based on the metrics specified.
    """

    class Meta:
        create_url = "/apis/autoscaling/v2beta1/namespaces/{namespace}/horizontalpodautoscalers"
        delete_url = "/apis/autoscaling/v2beta1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        get_url = "/apis/autoscaling/v2beta1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        list_all_url = "/apis/autoscaling/v2beta1/horizontalpodautoscalers"
        list_ns_url = "/apis/autoscaling/v2beta1/namespaces/{namespace}/horizontalpodautoscalers"
        update_url = "/apis/autoscaling/v2beta1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watch_url = "/apis/autoscaling/v2beta1/watch/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watchlist_all_url = "/apis/autoscaling/v2beta1/watch/horizontalpodautoscalers"
        watchlist_ns_url = "/apis/autoscaling/v2beta1/watch/namespaces/{namespace}/horizontalpodautoscalers"

    apiVersion = Field(six.text_type, "autoscaling/v2beta1")
    kind = Field(six.text_type, "HorizontalPodAutoscaler")

    metadata = Field(ObjectMeta)
    spec = Field(HorizontalPodAutoscalerSpec)
    status = Field(HorizontalPodAutoscalerStatus)


class HorizontalPodAutoscalerList(Model):
    """
    HorizontalPodAutoscaler is a list of horizontal pod autoscaler objects.
    """
    apiVersion = Field(six.text_type, "autoscaling/v2beta1")
    kind = Field(six.text_type, "HorizontalPodAutoscalerList")

    items = ListField(HorizontalPodAutoscaler)
    metadata = Field(ListMeta)
