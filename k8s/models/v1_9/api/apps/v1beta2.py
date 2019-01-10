#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_9.api.core.v1 import PersistentVolumeClaim, PodTemplateSpec
from k8s.models.v1_9.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta
from k8s.models.v1_9.apimachinery.runtime import RawExtension


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class StatefulSetCondition(Model):
    """
    StatefulSetCondition describes the state of a statefulset at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class StatefulSetStatus(Model):
    """
    StatefulSetStatus represents the current state of a StatefulSet.
    """

    collisionCount = Field(int)
    conditions = ListField(StatefulSetCondition)
    currentReplicas = Field(int)
    currentRevision = Field(six.text_type)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = RequiredField(int)
    updateRevision = Field(six.text_type)
    updatedReplicas = Field(int)


class ScaleStatus(Model):
    """
    ScaleStatus represents the current status of a scale subresource.
    """

    replicas = RequiredField(int)
    selector = Field(dict)
    targetSelector = Field(six.text_type)


class ScaleSpec(Model):
    """
    ScaleSpec describes the attributes of a scale subresource
    """

    replicas = Field(int)


class Scale(Model):
    """
    Scale represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = ReadOnlyField(ScaleStatus)


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
    selector = RequiredField(LabelSelector)
    serviceName = RequiredField(six.text_type)
    template = RequiredField(PodTemplateSpec)
    updateStrategy = Field(StatefulSetUpdateStrategy)
    volumeClaimTemplates = ListField(PersistentVolumeClaim)


class StatefulSet(Model):
    """
    DEPRECATED - This group version of StatefulSet is deprecated by
    apps/v1/StatefulSet. See the release notes for more information. StatefulSet
    represents a set of pods with consistent identities. Identities are defined as:
    - Network: A single stable DNS and hostname.
     - Storage: As many VolumeClaims
    as requested.
    The StatefulSet guarantees that a given network identity will
    always map to the same storage identity.
    """

    class Meta:
        create_url = "/apis/apps/v1beta2/namespaces/{namespace}/statefulsets"
        delete_url = "/apis/apps/v1beta2/namespaces/{namespace}/statefulsets/{name}"
        get_url = "/apis/apps/v1beta2/namespaces/{namespace}/statefulsets/{name}"
        list_all_url = "/apis/apps/v1beta2/statefulsets"
        list_ns_url = "/apis/apps/v1beta2/namespaces/{namespace}/statefulsets"
        update_url = "/apis/apps/v1beta2/namespaces/{namespace}/statefulsets/{name}"
        watch_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/statefulsets/{name}"
        watchlist_all_url = "/apis/apps/v1beta2/watch/statefulsets"
        watchlist_ns_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/statefulsets"

    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "StatefulSet")

    metadata = Field(ObjectMeta)
    spec = Field(StatefulSetSpec)
    status = Field(StatefulSetStatus)


class StatefulSetList(Model):
    """
    StatefulSetList is a collection of StatefulSets.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "StatefulSetList")

    items = ListField(StatefulSet)
    metadata = Field(ListMeta)


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
    selector = RequiredField(LabelSelector)
    strategy = Field(DeploymentStrategy)
    template = RequiredField(PodTemplateSpec)


class RollingUpdateDaemonSet(Model):
    """
    Spec to control the desired behavior of daemon set rolling update.
    """

    maxUnavailable = Field(six.text_type, alt_type=int)


class DaemonSetUpdateStrategy(Model):
    """
    DaemonSetUpdateStrategy is a struct used to control the update strategy for a
    DaemonSet.
    """

    rollingUpdate = Field(RollingUpdateDaemonSet)
    type = Field(six.text_type)


class DaemonSetSpec(Model):
    """
    DaemonSetSpec is the specification of a daemon set.
    """

    minReadySeconds = Field(int)
    revisionHistoryLimit = Field(int)
    selector = RequiredField(LabelSelector)
    template = RequiredField(PodTemplateSpec)
    updateStrategy = Field(DaemonSetUpdateStrategy)


class ReplicaSetSpec(Model):
    """
    ReplicaSetSpec is the specification of a ReplicaSet.
    """

    minReadySeconds = Field(int)
    replicas = Field(int)
    selector = RequiredField(LabelSelector)
    template = Field(PodTemplateSpec)


class ReplicaSetCondition(Model):
    """
    ReplicaSetCondition describes the state of a replica set at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class ReplicaSetStatus(Model):
    """
    ReplicaSetStatus represents the current status of a ReplicaSet.
    """

    availableReplicas = Field(int)
    conditions = ListField(ReplicaSetCondition)
    fullyLabeledReplicas = Field(int)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = RequiredField(int)


class ReplicaSet(Model):
    """
    DEPRECATED - This group version of ReplicaSet is deprecated by
    apps/v1/ReplicaSet. See the release notes for more information. ReplicaSet
    ensures that a specified number of pod replicas are running at any given time.
    """

    class Meta:
        create_url = "/apis/apps/v1beta2/namespaces/{namespace}/replicasets"
        delete_url = "/apis/apps/v1beta2/namespaces/{namespace}/replicasets/{name}"
        get_url = "/apis/apps/v1beta2/namespaces/{namespace}/replicasets/{name}"
        list_all_url = "/apis/apps/v1beta2/replicasets"
        list_ns_url = "/apis/apps/v1beta2/namespaces/{namespace}/replicasets"
        update_url = "/apis/apps/v1beta2/namespaces/{namespace}/replicasets/{name}"
        watch_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/replicasets/{name}"
        watchlist_all_url = "/apis/apps/v1beta2/watch/replicasets"
        watchlist_ns_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/replicasets"

    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "ReplicaSet")

    metadata = Field(ObjectMeta)
    spec = Field(ReplicaSetSpec)
    status = ReadOnlyField(ReplicaSetStatus)


class ReplicaSetList(Model):
    """
    ReplicaSetList is a collection of ReplicaSets.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "ReplicaSetList")

    items = ListField(ReplicaSet)
    metadata = Field(ListMeta)


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


class Deployment(Model):
    """
    DEPRECATED - This group version of Deployment is deprecated by
    apps/v1/Deployment. See the release notes for more information. Deployment
    enables declarative updates for Pods and ReplicaSets.
    """

    class Meta:
        create_url = "/apis/apps/v1beta2/namespaces/{namespace}/deployments"
        delete_url = "/apis/apps/v1beta2/namespaces/{namespace}/deployments/{name}"
        get_url = "/apis/apps/v1beta2/namespaces/{namespace}/deployments/{name}"
        list_all_url = "/apis/apps/v1beta2/deployments"
        list_ns_url = "/apis/apps/v1beta2/namespaces/{namespace}/deployments"
        update_url = "/apis/apps/v1beta2/namespaces/{namespace}/deployments/{name}"
        watch_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/deployments/{name}"
        watchlist_all_url = "/apis/apps/v1beta2/watch/deployments"
        watchlist_ns_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/deployments"

    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "Deployment")

    metadata = Field(ObjectMeta)
    spec = Field(DeploymentSpec)
    status = Field(DeploymentStatus)


class DeploymentList(Model):
    """
    DeploymentList is a list of Deployments.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "DeploymentList")

    items = ListField(Deployment)
    metadata = Field(ListMeta)


class DaemonSetCondition(Model):
    """
    DaemonSetCondition describes the state of a DaemonSet at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class DaemonSetStatus(Model):
    """
    DaemonSetStatus represents the current status of a daemon set.
    """

    collisionCount = Field(int)
    conditions = ListField(DaemonSetCondition)
    currentNumberScheduled = RequiredField(int)
    desiredNumberScheduled = RequiredField(int)
    numberAvailable = Field(int)
    numberMisscheduled = RequiredField(int)
    numberReady = RequiredField(int)
    numberUnavailable = Field(int)
    observedGeneration = Field(int)
    updatedNumberScheduled = Field(int)


class DaemonSet(Model):
    """
    DEPRECATED - This group version of DaemonSet is deprecated by
    apps/v1/DaemonSet. See the release notes for more information. DaemonSet
    represents the configuration of a daemon set.
    """

    class Meta:
        create_url = "/apis/apps/v1beta2/namespaces/{namespace}/daemonsets"
        delete_url = "/apis/apps/v1beta2/namespaces/{namespace}/daemonsets/{name}"
        get_url = "/apis/apps/v1beta2/namespaces/{namespace}/daemonsets/{name}"
        list_all_url = "/apis/apps/v1beta2/daemonsets"
        list_ns_url = "/apis/apps/v1beta2/namespaces/{namespace}/daemonsets"
        update_url = "/apis/apps/v1beta2/namespaces/{namespace}/daemonsets/{name}"
        watch_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/daemonsets/{name}"
        watchlist_all_url = "/apis/apps/v1beta2/watch/daemonsets"
        watchlist_ns_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/daemonsets"

    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "DaemonSet")

    metadata = Field(ObjectMeta)
    spec = Field(DaemonSetSpec)
    status = ReadOnlyField(DaemonSetStatus)


class DaemonSetList(Model):
    """
    DaemonSetList is a collection of daemon sets.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "DaemonSetList")

    items = ListField(DaemonSet)
    metadata = Field(ListMeta)


class ControllerRevision(Model):
    """
    DEPRECATED - This group version of ControllerRevision is deprecated by
    apps/v1/ControllerRevision. See the release notes for more information.
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
        create_url = "/apis/apps/v1beta2/namespaces/{namespace}/controllerrevisions"
        delete_url = "/apis/apps/v1beta2/namespaces/{namespace}/controllerrevisions/{name}"
        get_url = "/apis/apps/v1beta2/namespaces/{namespace}/controllerrevisions/{name}"
        list_all_url = "/apis/apps/v1beta2/controllerrevisions"
        list_ns_url = "/apis/apps/v1beta2/namespaces/{namespace}/controllerrevisions"
        update_url = "/apis/apps/v1beta2/namespaces/{namespace}/controllerrevisions/{name}"
        watch_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/controllerrevisions/{name}"
        watchlist_all_url = "/apis/apps/v1beta2/watch/controllerrevisions"
        watchlist_ns_url = "/apis/apps/v1beta2/watch/namespaces/{namespace}/controllerrevisions"

    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "ControllerRevision")

    data = Field(RawExtension)
    metadata = Field(ObjectMeta)
    revision = RequiredField(int)


class ControllerRevisionList(Model):
    """
    ControllerRevisionList is a resource containing a list of ControllerRevision
    objects.
    """
    apiVersion = Field(six.text_type, "apps/v1beta2")
    kind = Field(six.text_type, "ControllerRevisionList")

    items = ListField(ControllerRevision)
    metadata = Field(ListMeta)
