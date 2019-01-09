#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta
from k8s.models.v1_7.apimachinery.runtime import RawExtension
from k8s.models.v1_7.kubernetes.api.v1 import PersistentVolumeClaim, PodTemplateSpec


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
    selector = Field(dict)
    targetSelector = Field(six.text_type)


class RollingUpdateStatefulSetStrategy(Model):
    """
    RollingUpdateStatefulSetStrategy is used to communicate parameter for
    RollingUpdateStatefulSetStrategyType.
    """

    partition = Field(int)


class StatefulSetUpdateStrategy(Model):
    """
    StatefulSetUpdateStrategy indicates the strategy that the StatefulSet
    controller will use to perform updates. It includes any additional parameters
    necessary to perform the update for the indicated strategy.
    """

    rollingUpdate = Field(RollingUpdateStatefulSetStrategy)
    type = Field(six.text_type)


class StatefulSetSpec(Model):
    """
    A StatefulSetSpec is the specification of a StatefulSet.
    """

    podManagementPolicy = Field(six.text_type)
    replicas = Field(int)
    revisionHistoryLimit = Field(int)
    selector = Field(LabelSelector)
    serviceName = RequiredField(six.text_type)
    template = RequiredField(PodTemplateSpec)
    updateStrategy = Field(StatefulSetUpdateStrategy)
    volumeClaimTemplates = ListField(PersistentVolumeClaim)


class ControllerRevision(Model):
    """
    ControllerRevision implements an immutable snapshot of state data. Clients are
    responsible for serializing and deserializing the objects that contain their
    internal state. Once a ControllerRevision has been successfully created, it can
    not be updated. The API Server will fail validation of all requests that
    attempt to mutate the Data field. ControllerRevisions may, however, be deleted.
    Note that, due to its use by both the DaemonSet and StatefulSet controllers for
    update and rollback, this object is beta. However, it may be subject to name
    and representation changes in future releases, and clients should not depend on
    its stability. It is primarily for internal use by controllers.
    """
    class Meta:
        create_url = "/apis/apps/v1beta1/namespaces/{namespace}/controllerrevisions"
        delete_url = "/apis/apps/v1beta1/namespaces/{namespace}/controllerrevisions/{name}"
        get_url = "/apis/apps/v1beta1/namespaces/{namespace}/controllerrevisions/{name}"
        list_all_url = "/apis/apps/v1beta1/controllerrevisions"
        list_ns_url = "/apis/apps/v1beta1/namespaces/{namespace}/controllerrevisions"
        update_url = "/apis/apps/v1beta1/namespaces/{namespace}/controllerrevisions/{name}"
        watch_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/controllerrevisions/{name}"
        watchlist_all_url = "/apis/apps/v1beta1/watch/controllerrevisions"
        watchlist_ns_url = "/apis/apps/v1beta1/watch/namespaces/{namespace}/controllerrevisions"
    
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "ControllerRevision")

    data = Field(RawExtension)
    metadata = Field(ObjectMeta)
    revision = RequiredField(int)


class ControllerRevisionList(Model):
    """
    ControllerRevisionList is a resource containing a list of ControllerRevision
    objects.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "ControllerRevisionList")

    items = ListField(ControllerRevision)
    metadata = Field(ListMeta)


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

    name = RequiredField(six.text_type)
    rollbackTo = RequiredField(RollbackConfig)
    updatedAnnotations = Field(dict)


class StatefulSetStatus(Model):
    """
    StatefulSetStatus represents the current state of a StatefulSet.
    """

    currentReplicas = Field(int)
    currentRevision = Field(six.text_type)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = RequiredField(int)
    updateRevision = Field(six.text_type)
    updatedReplicas = Field(int)


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


class ScaleSpec(Model):
    """
    ScaleSpec describes the attributes of a scale subresource
    """

    replicas = Field(int)


class Scale(Model):
    """
    Scale represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "apps/v1beta1")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = ReadOnlyField(ScaleStatus)


class DeploymentCondition(Model):
    """
    DeploymentCondition describes the state of a deployment at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    lastUpdateTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class DeploymentStatus(Model):
    """
    DeploymentStatus is the most recently observed status of the Deployment.
    """

    availableReplicas = Field(int)
    collisionCount = Field(int)
    conditions = ListField(DeploymentCondition)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = Field(int)
    unavailableReplicas = Field(int)
    updatedReplicas = Field(int)


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
    template = RequiredField(PodTemplateSpec)


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

