#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import PersistentVolumeClaim, PodTemplateSpec


class RollbackConfig(Model):
    """
    
    """

    revision = Field(int)


class DeploymentRollback(Model):
    """
    DeploymentRollback stores the information required to rollback a deployment.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "DeploymentRollback")

    name = Field(six.text_type)
    rollbackTo = Field(RollbackConfig)
    updatedAnnotations = Field(dict)


class RollingUpdateDeployment(Model):
    """
    Spec to control the desired behavior of rolling update.
    """

    maxSurge = Field(six.text_type, alt_type=int)
    maxUnavailable = Field(six.text_type, alt_type=int)


class DeploymentStrategy(Model):
    """
    DeploymentStrategy describes how to replace existing pods with new ones.
    """

    rollingUpdate = Field(RollingUpdateDeployment)
    type = Field(six.text_type)


class DeploymentSpec(Model):
    """
    DeploymentSpec is the specification of the desired behavior of the Deployment.
    """

    minReadySeconds = Field(int)
    paused = Field(bool)
    progressDeadlineSeconds = Field(int)
    replicas = Field(int)
    revisionHistoryLimit = Field(int)
    rollbackTo = Field(RollbackConfig)
    selector = Field(LabelSelector)
    strategy = Field(DeploymentStrategy)
    template = Field(PodTemplateSpec)


class StatefulSetSpec(Model):
    """
    A StatefulSetSpec is the specification of a StatefulSet.
    """

    replicas = Field(int)
    selector = Field(LabelSelector)
    serviceName = Field(six.text_type)
    template = Field(PodTemplateSpec)
    volumeClaimTemplates = ListField(PersistentVolumeClaim)


class ScaleSpec(Model):
    """
    ScaleSpec describes the attributes of a scale subresource
    """

    replicas = Field(int)


class StatefulSetStatus(Model):
    """
    StatefulSetStatus represents the current state of a StatefulSet.
    """

    observedGeneration = Field(int)
    replicas = Field(int)


class StatefulSet(Model):
    """
    StatefulSet represents a set of pods with consistent identities. Identities are
    defined as:
     - Network: A single stable DNS and hostname.
     - Storage: As many
    VolumeClaims as requested.
    The StatefulSet guarantees that a given network
    identity will always map to the same storage identity.
    """
    class Meta:
        create_url = "/apis/apps/v1beta1/namespaces/{namespace}/statefulsets"
        delete_url = "/apis/apps/v1beta1/namespaces/{namespace}/statefulsets/{name}"
        get_url = "/apis/apps/v1beta1/namespaces/{namespace}/statefulsets/{name}"
        list_all_url = "/apis/apps/v1beta1/statefulsets"
        list_ns_url = "/apis/apps/v1beta1/namespaces/{namespace}/statefulsets"
        update_url = "/apis/apps/v1beta1/namespaces/{namespace}/statefulsets/{name}"
        watch_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/statefulsets/{name}"
        watchlist_all_url = "/apis/apps/v1beta1/watch/statefulsets"
        watchlist_ns_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/statefulsets"
    
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "StatefulSet")

    metadata = Field(ObjectMeta)
    spec = Field(StatefulSetSpec)
    status = Field(StatefulSetStatus)


class StatefulSetList(Model):
    """
    StatefulSetList is a collection of StatefulSets.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "StatefulSetList")

    items = ListField(StatefulSet)
    metadata = Field(ListMeta)


class DeploymentCondition(Model):
    """
    DeploymentCondition describes the state of a deployment at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    lastUpdateTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = Field(six.text_type)
    type = Field(six.text_type)


class DeploymentStatus(Model):
    """
    DeploymentStatus is the most recently observed status of the Deployment.
    """

    availableReplicas = Field(int)
    conditions = ListField(DeploymentCondition)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = Field(int)
    unavailableReplicas = Field(int)
    updatedReplicas = Field(int)


class Deployment(Model):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.
    """
    class Meta:
        create_url = "/apis/apps/v1beta1/namespaces/{namespace}/deployments"
        delete_url = "/apis/apps/v1beta1/namespaces/{namespace}/deployments/{name}"
        get_url = "/apis/apps/v1beta1/namespaces/{namespace}/deployments/{name}"
        list_all_url = "/apis/apps/v1beta1/deployments"
        list_ns_url = "/apis/apps/v1beta1/namespaces/{namespace}/deployments"
        update_url = "/apis/apps/v1beta1/namespaces/{namespace}/deployments/{name}"
        watch_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/deployments/{name}"
        watchlist_all_url = "/apis/apps/v1beta1/watch/deployments"
        watchlist_ns_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/deployments"
    
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "Deployment")

    metadata = Field(ObjectMeta)
    spec = Field(DeploymentSpec)
    status = Field(DeploymentStatus)


class DeploymentList(Model):
    """
    DeploymentList is a list of Deployments.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "DeploymentList")

    items = ListField(Deployment)
    metadata = Field(ListMeta)


class ScaleStatus(Model):
    """
    ScaleStatus represents the current status of a scale subresource.
    """

    replicas = Field(int)
    selector = Field(dict)
    targetSelector = Field(six.text_type)


class Scale(Model):
    """
    Scale represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = Field(ScaleStatus)

