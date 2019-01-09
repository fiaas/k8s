#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


class CrossVersionObjectReference(Model):
    """
    CrossVersionObjectReference contains enough information to let you identify the
    referred resource.
    """

    name = Field(six.text_type)


class ObjectMetricStatus(Model):
    """
    ObjectMetricStatus indicates the current value of a metric describing a
    kubernetes object (for example, hits-per-second on an Ingress object).
    """

    currentValue = Field(six.text_type)
    metricName = Field(six.text_type)
    target = Field(CrossVersionObjectReference)


class ObjectMetricSource(Model):
    """
    ObjectMetricSource indicates how to scale on a metric describing a kubernetes
    object (for example, hits-per-second on an Ingress object).
    """

    metricName = Field(six.text_type)
    target = Field(CrossVersionObjectReference)
    targetValue = Field(six.text_type)


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

    name = Field(six.text_type)
    targetAverageUtilization = Field(int)
    targetAverageValue = Field(six.text_type)


class ResourceMetricStatus(Model):
    """
    ResourceMetricStatus indicates the current value of a resource metric known to
    Kubernetes, as specified in requests and limits, describing each pod in the
    current scale target (e.g. CPU or memory).  Such metrics are built in to
    Kubernetes, and have special scaling options on top of those available to
    normal per-pod metrics using the 'pods' source.
    """

    currentAverageUtilization = Field(int)
    currentAverageValue = Field(six.text_type)
    name = Field(six.text_type)


class PodsMetricSource(Model):
    """
    PodsMetricSource indicates how to scale on a metric describing each pod in the
    current scale target (for example, transactions-processed-per-second). The
    values will be averaged together before being compared to the target value.
    """

    metricName = Field(six.text_type)
    targetAverageValue = Field(six.text_type)


class MetricSpec(Model):
    """
    MetricSpec specifies how to scale based on a single metric (only `type` and one
    other matching field should be set at once).
    """

    object = Field(ObjectMetricSource)
    pods = Field(PodsMetricSource)
    resource = Field(ResourceMetricSource)
    type = Field(six.text_type)


class HorizontalPodAutoscalerSpec(Model):
    """
    HorizontalPodAutoscalerSpec describes the desired functionality of the
    HorizontalPodAutoscaler.
    """

    maxReplicas = Field(int)
    metrics = ListField(MetricSpec)
    minReplicas = Field(int)
    scaleTargetRef = Field(CrossVersionObjectReference)


class PodsMetricStatus(Model):
    """
    PodsMetricStatus indicates the current value of a metric describing each pod in
    the current scale target (for example, transactions-processed-per-second).
    """

    currentAverageValue = Field(six.text_type)
    metricName = Field(six.text_type)


class MetricStatus(Model):
    """
    MetricStatus describes the last-read state of a single metric.
    """

    object = Field(ObjectMetricStatus)
    pods = Field(PodsMetricStatus)
    resource = Field(ResourceMetricStatus)
    type = Field(six.text_type)


class HorizontalPodAutoscalerStatus(Model):
    """
    HorizontalPodAutoscalerStatus describes the current status of a horizontal pod
    autoscaler.
    """

    currentMetrics = ListField(MetricStatus)
    currentReplicas = Field(int)
    desiredReplicas = Field(int)
    lastScaleTime = Field(datetime.datetime)
    observedGeneration = Field(int)


class HorizontalPodAutoscaler(Model):
    """
    HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler,
    which automatically manages the replica count of any resource implementing the
    scale subresource based on the metrics specified.
    """
    class Meta:
        create_url = "/apis/autoscaling/v2alpha1/namespaces/{namespace}/horizontalpodautoscalers"
        delete_url = "/apis/autoscaling/v2alpha1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        get_url = "/apis/autoscaling/v2alpha1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        list_all_url = "/apis/autoscaling/v2alpha1/horizontalpodautoscalers"
        list_ns_url = "/apis/autoscaling/v2alpha1/namespaces/{namespace}/horizontalpodautoscalers"
        update_url = "/apis/autoscaling/v2alpha1/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watch_url = "/apis/autoscaling/v2alpha1/watch/namespaces/{namespace}/horizontalpodautoscalers/{name}"
        watchlist_all_url = "/apis/autoscaling/v2alpha1/watch/horizontalpodautoscalers"
        watchlist_ns_url = "/apis/autoscaling/v2alpha1/watch/namespaces/{namespace}/horizontalpodautoscalers"
    
    apiVersion = Field(six.text_type, "autoscaling/v2alpha1")
    kind = Field(six.text_type, "HorizontalPodAutoscaler")

    metadata = Field(ObjectMeta)
    spec = Field(HorizontalPodAutoscalerSpec)
    status = Field(HorizontalPodAutoscalerStatus)


class HorizontalPodAutoscalerList(Model):
    """
    HorizontalPodAutoscaler is a list of horizontal pod autoscaler objects.
    """
    apiVersion = Field(six.text_type, "autoscaling/v2alpha1")
    kind = Field(six.text_type, "HorizontalPodAutoscalerList")

    items = ListField(HorizontalPodAutoscaler)
    metadata = Field(ListMeta)

