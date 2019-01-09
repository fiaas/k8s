#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class VsphereVirtualDiskVolumeSource(Model):
    """
    Represents a vSphere volume resource.
    """

    fsType = Field(six.text_type)
    volumePath = RequiredField(six.text_type)


class VolumeMount(Model):
    """
    VolumeMount describes a mounting of a Volume within a container.
    """

    mountPath = RequiredField(six.text_type)
    name = RequiredField(six.text_type)
    readOnly = Field(bool)
    subPath = Field(six.text_type)


class Toleration(Model):
    """
    The pod this Toleration is attached to tolerates any taint that matches the
    triple <key,value,effect> using the matching operator <operator>.
    """

    effect = Field(six.text_type)
    key = Field(six.text_type)
    operator = Field(six.text_type)
    tolerationSeconds = Field(int)
    value = Field(six.text_type)


class Taint(Model):
    """
    The node this Taint is attached to has the effect 'effect' on any pod that that
    does not tolerate the Taint.
    """

    effect = RequiredField(six.text_type)
    key = RequiredField(six.text_type)
    timeAdded = Field(datetime.datetime)
    value = Field(six.text_type)


class NodeSpec(Model):
    """
    NodeSpec describes the attributes that a node is created with.
    """

    externalID = Field(six.text_type)
    podCIDR = Field(six.text_type)
    providerID = Field(six.text_type)
    taints = ListField(Taint)
    unschedulable = Field(bool)


class TCPSocketAction(Model):
    """
    TCPSocketAction describes an action based on opening a socket
    """

    port = RequiredField(six.text_type, alt_type=int)


class ServicePort(Model):
    """
    ServicePort contains information on service's port.
    """

    name = Field(six.text_type)
    nodePort = Field(int)
    port = RequiredField(int)
    protocol = Field(six.text_type)
    targetPort = Field(six.text_type, alt_type=int)


class ServiceSpec(Model):
    """
    ServiceSpec describes the attributes that a user creates on a service.
    """

    clusterIP = Field(six.text_type)
    deprecatedPublicIPs = ListField(six.text_type)
    externalIPs = ListField(six.text_type)
    externalName = Field(six.text_type)
    loadBalancerIP = Field(six.text_type)
    loadBalancerSourceRanges = ListField(six.text_type)
    ports = ListField(ServicePort)
    selector = Field(dict)
    sessionAffinity = Field(six.text_type)
    type = Field(six.text_type)


class SecretKeySelector(Model):
    """
    SecretKeySelector selects a key of a Secret.
    """

    key = RequiredField(six.text_type)
    name = Field(six.text_type)
    optional = Field(bool)


class SecretEnvSource(Model):
    """
    SecretEnvSource selects a Secret to populate the environment variables with.
    The contents of the target Secret's Data field will represent the key-value
    pairs as environment variables.
    """

    name = Field(six.text_type)
    optional = Field(bool)


class Secret(Model):
    """
    Secret holds secret data of a certain type. The total bytes of the values in
    the Data field must be less than MaxSecretSize bytes.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/secrets"
        delete_url = "/api/v1/namespaces/{namespace}/secrets/{name}"
        get_url = "/api/v1/namespaces/{namespace}/secrets/{name}"
        list_all_url = "/api/v1/secrets"
        list_ns_url = "/api/v1/namespaces/{namespace}/secrets"
        update_url = "/api/v1/namespaces/{namespace}/secrets/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/secrets/{name}"
        watchlist_all_url = "/api/v1/watch/secrets"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/secrets"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Secret")

    data = Field(dict)
    metadata = Field(ObjectMeta)
    stringData = Field(dict)
    type = Field(six.text_type)


class SecretList(Model):
    """
    SecretList is a list of Secret.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "SecretList")

    items = ListField(Secret)
    metadata = Field(ListMeta)


class SELinuxOptions(Model):
    """
    SELinuxOptions are the labels to be applied to the container
    """

    level = Field(six.text_type)
    role = Field(six.text_type)
    type = Field(six.text_type)
    user = Field(six.text_type)


class PodSecurityContext(Model):
    """
    PodSecurityContext holds pod-level security attributes and common container
    settings. Some fields are also present in container.securityContext.  Field
    values of container.securityContext take precedence over field values of
    PodSecurityContext.
    """

    fsGroup = Field(int)
    runAsNonRoot = Field(bool)
    runAsUser = Field(int)
    seLinuxOptions = Field(SELinuxOptions)
    supplementalGroups = ListField(int)


class ResourceRequirements(Model):
    """
    ResourceRequirements describes the compute resource requirements.
    """

    limits = Field(dict)
    requests = Field(dict)


class PersistentVolumeClaimSpec(Model):
    """
    PersistentVolumeClaimSpec describes the common attributes of storage devices
    and allows a Source for provider-specific attributes
    """

    accessModes = ListField(six.text_type)
    resources = Field(ResourceRequirements)
    selector = Field(LabelSelector)
    storageClassName = Field(six.text_type)
    volumeName = Field(six.text_type)


class ResourceQuotaStatus(Model):
    """
    ResourceQuotaStatus defines the enforced hard limits and observed use.
    """

    hard = Field(dict)
    used = Field(dict)


class ResourceQuotaSpec(Model):
    """
    ResourceQuotaSpec defines the desired hard limits to enforce for Quota.
    """

    hard = Field(dict)
    scopes = ListField(six.text_type)


class ResourceQuota(Model):
    """
    ResourceQuota sets aggregate quota restrictions enforced per namespace
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/resourcequotas"
        delete_url = "/api/v1/namespaces/{namespace}/resourcequotas/{name}"
        get_url = "/api/v1/namespaces/{namespace}/resourcequotas/{name}"
        list_all_url = "/api/v1/resourcequotas"
        list_ns_url = "/api/v1/namespaces/{namespace}/resourcequotas"
        update_url = "/api/v1/namespaces/{namespace}/resourcequotas/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/resourcequotas/{name}"
        watchlist_all_url = "/api/v1/watch/resourcequotas"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/resourcequotas"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ResourceQuota")

    metadata = Field(ObjectMeta)
    spec = Field(ResourceQuotaSpec)
    status = Field(ResourceQuotaStatus)


class ResourceQuotaList(Model):
    """
    ResourceQuotaList is a list of ResourceQuota items.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ResourceQuotaList")

    items = ListField(ResourceQuota)
    metadata = Field(ListMeta)


class ResourceFieldSelector(Model):
    """
    ResourceFieldSelector represents container resources (cpu, memory) and their
    output format
    """

    containerName = Field(six.text_type)
    divisor = Field(six.text_type)
    resource = RequiredField(six.text_type)


class ReplicationControllerCondition(Model):
    """
    ReplicationControllerCondition describes the state of a replication controller
    at a certain point.
    """

    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class ReplicationControllerStatus(Model):
    """
    ReplicationControllerStatus represents the current status of a replication
    controller.
    """

    availableReplicas = Field(int)
    conditions = ListField(ReplicationControllerCondition)
    fullyLabeledReplicas = Field(int)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = RequiredField(int)


class QuobyteVolumeSource(Model):
    """
    Represents a Quobyte mount that lasts the lifetime of a pod. Quobyte volumes do
    not support ownership management or SELinux relabeling.
    """

    group = Field(six.text_type)
    readOnly = Field(bool)
    registry = RequiredField(six.text_type)
    user = Field(six.text_type)
    volume = RequiredField(six.text_type)


class PortworxVolumeSource(Model):
    """
    PortworxVolumeSource represents a Portworx volume resource.
    """

    fsType = Field(six.text_type)
    readOnly = Field(bool)
    volumeID = RequiredField(six.text_type)


class PodCondition(Model):
    """
    PodCondition contains details for the current condition of this pod.
    """

    lastProbeTime = Field(datetime.datetime)
    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class PodAffinityTerm(Model):
    """
    Defines a set of pods (namely those matching the labelSelector relative to the
    given namespace(s)) that this pod should be co-located (affinity) or not co-
    located (anti-affinity) with, where co-located is defined as running on a node
    whose value of the label with key <topologyKey> tches that of any node on which
    a pod of the set of pods is running
    """

    labelSelector = Field(LabelSelector)
    namespaces = ListField(six.text_type)
    topologyKey = Field(six.text_type)


class WeightedPodAffinityTerm(Model):
    """
    The weights of all of the matched WeightedPodAffinityTerm fields are added per-
    node to find the most preferred node(s)
    """

    podAffinityTerm = RequiredField(PodAffinityTerm)
    weight = RequiredField(int)


class PodAntiAffinity(Model):
    """
    Pod anti affinity is a group of inter pod anti affinity scheduling rules.
    """

    preferredDuringSchedulingIgnoredDuringExecution = ListField(WeightedPodAffinityTerm)
    requiredDuringSchedulingIgnoredDuringExecution = ListField(PodAffinityTerm)


class PodAffinity(Model):
    """
    Pod affinity is a group of inter pod affinity scheduling rules.
    """

    preferredDuringSchedulingIgnoredDuringExecution = ListField(WeightedPodAffinityTerm)
    requiredDuringSchedulingIgnoredDuringExecution = ListField(PodAffinityTerm)


class PhotonPersistentDiskVolumeSource(Model):
    """
    Represents a Photon Controller persistent disk resource.
    """

    fsType = Field(six.text_type)
    pdID = RequiredField(six.text_type)


class PersistentVolumeStatus(Model):
    """
    PersistentVolumeStatus is the current status of a persistent volume.
    """

    message = Field(six.text_type)
    phase = Field(six.text_type)
    reason = Field(six.text_type)


class PersistentVolumeClaimVolumeSource(Model):
    """
    PersistentVolumeClaimVolumeSource references the user's PVC in the same
    namespace. This volume finds the bound PV and mounts that volume for the pod. A
    PersistentVolumeClaimVolumeSource is, essentially, a wrapper around another
    type of volume that is owned by someone else (the system).
    """

    claimName = RequiredField(six.text_type)
    readOnly = Field(bool)


class PersistentVolumeClaimStatus(Model):
    """
    PersistentVolumeClaimStatus is the current status of a persistent volume claim.
    """

    accessModes = ListField(six.text_type)
    capacity = Field(dict)
    phase = Field(six.text_type)


class PersistentVolumeClaim(Model):
    """
    PersistentVolumeClaim is a user's request for and claim to a persistent volume
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/persistentvolumeclaims"
        delete_url = "/api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}"
        get_url = "/api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}"
        list_all_url = "/api/v1/persistentvolumeclaims"
        list_ns_url = "/api/v1/namespaces/{namespace}/persistentvolumeclaims"
        update_url = "/api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/persistentvolumeclaims/{name}"
        watchlist_all_url = "/api/v1/watch/persistentvolumeclaims"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/persistentvolumeclaims"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PersistentVolumeClaim")

    metadata = Field(ObjectMeta)
    spec = Field(PersistentVolumeClaimSpec)
    status = ReadOnlyField(PersistentVolumeClaimStatus)


class PersistentVolumeClaimList(Model):
    """
    PersistentVolumeClaimList is a list of PersistentVolumeClaim items.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PersistentVolumeClaimList")

    items = ListField(PersistentVolumeClaim)
    metadata = Field(ListMeta)


class ObjectReference(Model):
    """
    ObjectReference contains enough information to let you inspect or modify the
    referred object.
    """

    fieldPath = Field(six.text_type)
    name = Field(six.text_type)
    namespace = Field(six.text_type)
    resourceVersion = Field(six.text_type)
    uid = Field(six.text_type)


class EndpointAddress(Model):
    """
    EndpointAddress is a tuple that describes single IP address.
    """

    hostname = Field(six.text_type)
    ip = RequiredField(six.text_type)
    nodeName = Field(six.text_type)
    targetRef = Field(ObjectReference)


class Binding(Model):
    """
    Binding ties one object to another. For example, a pod is bound to a node by a
    scheduler.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Binding")

    metadata = Field(ObjectMeta)
    target = RequiredField(ObjectReference)


class ObjectFieldSelector(Model):
    """
    ObjectFieldSelector selects an APIVersioned field of an object.
    """

    fieldPath = RequiredField(six.text_type)


class DownwardAPIVolumeFile(Model):
    """
    DownwardAPIVolumeFile represents information to create the file containing the
    pod field
    """

    fieldRef = Field(ObjectFieldSelector)
    mode = Field(int)
    path = RequiredField(six.text_type)
    resourceFieldRef = Field(ResourceFieldSelector)


class DownwardAPIVolumeSource(Model):
    """
    DownwardAPIVolumeSource represents a volume containing downward API info.
    Downward API volumes support ownership management and SELinux relabeling.
    """

    defaultMode = Field(int)
    items = ListField(DownwardAPIVolumeFile)


class DownwardAPIProjection(Model):
    """
    Represents downward API info for projecting into a projected volume. Note that
    this is identical to a downwardAPI volume source without the default mode.
    """

    items = ListField(DownwardAPIVolumeFile)


class NodeSystemInfo(Model):
    """
    NodeSystemInfo is a set of ids/uuids to uniquely identify the node.
    """

    architecture = RequiredField(six.text_type)
    bootID = RequiredField(six.text_type)
    containerRuntimeVersion = RequiredField(six.text_type)
    kernelVersion = RequiredField(six.text_type)
    kubeProxyVersion = RequiredField(six.text_type)
    kubeletVersion = RequiredField(six.text_type)
    machineID = RequiredField(six.text_type)
    operatingSystem = RequiredField(six.text_type)
    osImage = RequiredField(six.text_type)
    systemUUID = RequiredField(six.text_type)


class NodeSelectorRequirement(Model):
    """
    A node selector requirement is a selector that contains values, a key, and an
    operator that relates the key and values.
    """

    key = RequiredField(six.text_type)
    operator = RequiredField(six.text_type)
    values = ListField(six.text_type)


class NodeSelectorTerm(Model):
    """
    A null or empty node selector term matches no objects.
    """

    matchExpressions = ListField(NodeSelectorRequirement)


class PreferredSchedulingTerm(Model):
    """
    An empty preferred scheduling term matches all objects with implicit weight 0
    (i.e. it's a no-op). A null preferred scheduling term matches no objects (i.e.
    is also a no-op).
    """

    preference = RequiredField(NodeSelectorTerm)
    weight = RequiredField(int)


class NodeSelector(Model):
    """
    A node selector represents the union of the results of one or more label
    queries over a set of nodes; that is, it represents the OR of the selectors
    represented by the node selector terms.
    """

    nodeSelectorTerms = ListField(NodeSelectorTerm)


class NodeAffinity(Model):
    """
    Node affinity is a group of node affinity scheduling rules.
    """

    preferredDuringSchedulingIgnoredDuringExecution = ListField(PreferredSchedulingTerm)
    requiredDuringSchedulingIgnoredDuringExecution = Field(NodeSelector)


class Affinity(Model):
    """
    Affinity is a group of affinity scheduling rules.
    """

    nodeAffinity = Field(NodeAffinity)
    podAffinity = Field(PodAffinity)
    podAntiAffinity = Field(PodAntiAffinity)


class NodeCondition(Model):
    """
    NodeCondition contains condition information for a node.
    """

    lastHeartbeatTime = Field(datetime.datetime)
    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class NodeAddress(Model):
    """
    NodeAddress contains information for the node's address.
    """

    address = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class NamespaceStatus(Model):
    """
    NamespaceStatus is information about the current status of a Namespace.
    """

    phase = Field(six.text_type)


class NamespaceSpec(Model):
    """
    NamespaceSpec describes the attributes on a Namespace.
    """

    finalizers = ListField(six.text_type)


class Namespace(Model):
    """
    Namespace provides a scope for Names. Use of multiple namespaces is optional.
    """
    class Meta:
        create_url = "/api/v1/namespaces"
        delete_url = "/api/v1/namespaces/{name}"
        get_url = "/api/v1/namespaces/{name}"
        list_all_url = "/api/v1/namespaces"
        update_url = "/api/v1/namespaces/{name}"
        update_url = "/api/v1/namespaces/{name}/finalize"
        watch_url = "/api/v1/watch/namespaces/{name}"
        watchlist_all_url = "/api/v1/watch/namespaces"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Namespace")

    metadata = Field(ObjectMeta)
    spec = Field(NamespaceSpec)
    status = Field(NamespaceStatus)


class NamespaceList(Model):
    """
    NamespaceList is a list of Namespaces.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "NamespaceList")

    items = ListField(Namespace)
    metadata = Field(ListMeta)


class NFSVolumeSource(Model):
    """
    Represents an NFS mount that lasts the lifetime of a pod. NFS volumes do not
    support ownership management or SELinux relabeling.
    """

    path = RequiredField(six.text_type)
    readOnly = Field(bool)
    server = RequiredField(six.text_type)


class LocalObjectReference(Model):
    """
    LocalObjectReference contains enough information to let you locate the
    referenced object inside the same namespace.
    """

    name = Field(six.text_type)


class ServiceAccount(Model):
    """
    ServiceAccount binds together: * a name, understood by users, and perhaps by
    peripheral systems, for an identity * a principal that can be authenticated and
    authorized * a set of secrets
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/serviceaccounts"
        delete_url = "/api/v1/namespaces/{namespace}/serviceaccounts/{name}"
        get_url = "/api/v1/namespaces/{namespace}/serviceaccounts/{name}"
        list_all_url = "/api/v1/serviceaccounts"
        list_ns_url = "/api/v1/namespaces/{namespace}/serviceaccounts"
        update_url = "/api/v1/namespaces/{namespace}/serviceaccounts/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/serviceaccounts/{name}"
        watchlist_all_url = "/api/v1/watch/serviceaccounts"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/serviceaccounts"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ServiceAccount")

    automountServiceAccountToken = Field(bool)
    imagePullSecrets = ListField(LocalObjectReference)
    metadata = Field(ObjectMeta)
    secrets = ListField(ObjectReference)


class ServiceAccountList(Model):
    """
    ServiceAccountList is a list of ServiceAccount objects
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ServiceAccountList")

    items = ListField(ServiceAccount)
    metadata = Field(ListMeta)


class ScaleIOVolumeSource(Model):
    """
    ScaleIOVolumeSource represents a persistent ScaleIO volume
    """

    fsType = Field(six.text_type)
    gateway = RequiredField(six.text_type)
    protectionDomain = Field(six.text_type)
    readOnly = Field(bool)
    secretRef = RequiredField(LocalObjectReference)
    sslEnabled = Field(bool)
    storageMode = Field(six.text_type)
    storagePool = Field(six.text_type)
    system = RequiredField(six.text_type)
    volumeName = Field(six.text_type)


class RBDVolumeSource(Model):
    """
    Represents a Rados Block Device mount that lasts the lifetime of a pod. RBD
    volumes support ownership management and SELinux relabeling.
    """

    fsType = Field(six.text_type)
    image = RequiredField(six.text_type)
    keyring = Field(six.text_type)
    monitors = ListField(six.text_type)
    pool = Field(six.text_type)
    readOnly = Field(bool)
    secretRef = Field(LocalObjectReference)
    user = Field(six.text_type)


class FlexVolumeSource(Model):
    """
    FlexVolume represents a generic volume resource that is provisioned/attached
    using an exec based plugin. This is an alpha feature and may change in future.
    """

    driver = RequiredField(six.text_type)
    fsType = Field(six.text_type)
    options = Field(dict)
    readOnly = Field(bool)
    secretRef = Field(LocalObjectReference)


class CephFSVolumeSource(Model):
    """
    Represents a Ceph Filesystem mount that lasts the lifetime of a pod Cephfs
    volumes do not support ownership management or SELinux relabeling.
    """

    monitors = ListField(six.text_type)
    path = Field(six.text_type)
    readOnly = Field(bool)
    secretFile = Field(six.text_type)
    secretRef = Field(LocalObjectReference)
    user = Field(six.text_type)


class LoadBalancerIngress(Model):
    """
    LoadBalancerIngress represents the status of a load-balancer ingress point:
    traffic intended for the service should be sent to an ingress point.
    """

    hostname = Field(six.text_type)
    ip = Field(six.text_type)


class LoadBalancerStatus(Model):
    """
    LoadBalancerStatus represents the status of a load-balancer.
    """

    ingress = ListField(LoadBalancerIngress)


class ServiceStatus(Model):
    """
    ServiceStatus represents the current status of a service.
    """

    loadBalancer = Field(LoadBalancerStatus)


class Service(Model):
    """
    Service is a named abstraction of software service (for example, mysql)
    consisting of local port (for example 3306) that the proxy listens on, and the
    selector that determines which pods will answer requests sent through the
    proxy.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/services"
        delete_url = "/api/v1/namespaces/{namespace}/services/{name}"
        get_url = "/api/v1/namespaces/{namespace}/services/{name}"
        list_all_url = "/api/v1/services"
        list_ns_url = "/api/v1/namespaces/{namespace}/services"
        update_url = "/api/v1/namespaces/{namespace}/services/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/services/{name}"
        watchlist_all_url = "/api/v1/watch/services"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/services"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Service")

    metadata = Field(ObjectMeta)
    spec = Field(ServiceSpec)
    status = ReadOnlyField(ServiceStatus)


class ServiceList(Model):
    """
    ServiceList holds a list of services.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ServiceList")

    items = ListField(Service)
    metadata = Field(ListMeta)


class LimitRangeItem(Model):
    """
    LimitRangeItem defines a min/max usage limit for any resource that matches on
    kind.
    """

    default = Field(dict)
    defaultRequest = Field(dict)
    max = Field(dict)
    maxLimitRequestRatio = Field(dict)
    min = Field(dict)
    type = Field(six.text_type)


class LimitRangeSpec(Model):
    """
    LimitRangeSpec defines a min/max usage limit for resources that match on kind.
    """

    limits = ListField(LimitRangeItem)


class LimitRange(Model):
    """
    LimitRange sets resource usage limits for each kind of resource in a Namespace.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/limitranges"
        delete_url = "/api/v1/namespaces/{namespace}/limitranges/{name}"
        get_url = "/api/v1/namespaces/{namespace}/limitranges/{name}"
        list_all_url = "/api/v1/limitranges"
        list_ns_url = "/api/v1/namespaces/{namespace}/limitranges"
        update_url = "/api/v1/namespaces/{namespace}/limitranges/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/limitranges/{name}"
        watchlist_all_url = "/api/v1/watch/limitranges"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/limitranges"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "LimitRange")

    metadata = Field(ObjectMeta)
    spec = Field(LimitRangeSpec)


class LimitRangeList(Model):
    """
    LimitRangeList is a list of LimitRange items.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "LimitRangeList")

    items = ListField(LimitRange)
    metadata = Field(ListMeta)


class KeyToPath(Model):
    """
    Maps a string key to a path within a volume.
    """

    key = RequiredField(six.text_type)
    mode = Field(int)
    path = RequiredField(six.text_type)


class SecretVolumeSource(Model):
    """
    Adapts a Secret into a volume.

    The contents of the target Secret's Data field
    will be presented in a volume as files using the keys in the Data field as the
    file names. Secret volumes support ownership management and SELinux relabeling.
    """

    defaultMode = Field(int)
    items = ListField(KeyToPath)
    optional = Field(bool)
    secretName = Field(six.text_type)


class SecretProjection(Model):
    """
    Adapts a secret into a projected volume.

    The contents of the target Secret's
    Data field will be presented in a projected volume as files using the keys in
    the Data field as the file names. Note that this is identical to a secret
    volume source without the default mode.
    """

    items = ListField(KeyToPath)
    name = Field(six.text_type)
    optional = Field(bool)


class ConfigMapVolumeSource(Model):
    """
    Adapts a ConfigMap into a volume.

    The contents of the target ConfigMap's Data
    field will be presented in a volume as files using the keys in the Data field
    as the file names, unless the items element is populated with specific mappings
    of keys to paths. ConfigMap volumes support ownership management and SELinux
    relabeling.
    """

    defaultMode = Field(int)
    items = ListField(KeyToPath)
    name = Field(six.text_type)
    optional = Field(bool)


class ConfigMapProjection(Model):
    """
    Adapts a ConfigMap into a projected volume.

    The contents of the target
    ConfigMap's Data field will be presented in a projected volume as files using
    the keys in the Data field as the file names, unless the items element is
    populated with specific mappings of keys to paths. Note that this is identical
    to a configmap volume source without the default mode.
    """

    items = ListField(KeyToPath)
    name = Field(six.text_type)
    optional = Field(bool)


class VolumeProjection(Model):
    """
    Projection that may be projected along with other supported volume types
    """

    configMap = Field(ConfigMapProjection)
    downwardAPI = Field(DownwardAPIProjection)
    secret = Field(SecretProjection)


class ProjectedVolumeSource(Model):
    """
    Represents a projected volume source
    """

    defaultMode = Field(int)
    sources = ListField(VolumeProjection)


class ISCSIVolumeSource(Model):
    """
    Represents an ISCSI disk. ISCSI volumes can only be mounted as read/write once.
    ISCSI volumes support ownership management and SELinux relabeling.
    """

    fsType = Field(six.text_type)
    iqn = RequiredField(six.text_type)
    iscsiInterface = Field(six.text_type)
    lun = RequiredField(int)
    portals = ListField(six.text_type)
    readOnly = Field(bool)
    targetPortal = RequiredField(six.text_type)


class HostPathVolumeSource(Model):
    """
    Represents a host path mapped into a pod. Host path volumes do not support
    ownership management or SELinux relabeling.
    """

    path = RequiredField(six.text_type)


class HTTPHeader(Model):
    """
    HTTPHeader describes a custom header to be used in HTTP probes
    """

    name = RequiredField(six.text_type)
    value = RequiredField(six.text_type)


class HTTPGetAction(Model):
    """
    HTTPGetAction describes an action based on HTTP Get requests.
    """

    host = Field(six.text_type)
    httpHeaders = ListField(HTTPHeader)
    path = Field(six.text_type)
    port = RequiredField(six.text_type, alt_type=int)
    scheme = Field(six.text_type)


class GlusterfsVolumeSource(Model):
    """
    Represents a Glusterfs mount that lasts the lifetime of a pod. Glusterfs
    volumes do not support ownership management or SELinux relabeling.
    """

    endpoints = RequiredField(six.text_type)
    path = RequiredField(six.text_type)
    readOnly = Field(bool)


class GitRepoVolumeSource(Model):
    """
    Represents a volume that is populated with the contents of a git repository.
    Git repo volumes do not support ownership management. Git repo volumes support
    SELinux relabeling.
    """

    directory = Field(six.text_type)
    repository = RequiredField(six.text_type)
    revision = Field(six.text_type)


class GCEPersistentDiskVolumeSource(Model):
    """
    Represents a Persistent Disk resource in Google Compute Engine.

    A GCE PD must
    exist before mounting to a container. The disk must also be in the same GCE
    project and zone as the kubelet. A GCE PD can only be mounted as read/write
    once or read-only many times. GCE PDs support ownership management and SELinux
    relabeling.
    """

    fsType = Field(six.text_type)
    partition = Field(int)
    pdName = RequiredField(six.text_type)
    readOnly = Field(bool)


class FlockerVolumeSource(Model):
    """
    Represents a Flocker volume mounted by the Flocker agent. One and only one of
    datasetName and datasetUUID should be set. Flocker volumes do not support
    ownership management or SELinux relabeling.
    """

    datasetName = Field(six.text_type)
    datasetUUID = Field(six.text_type)


class FCVolumeSource(Model):
    """
    Represents a Fibre Channel volume. Fibre Channel volumes can only be mounted as
    read/write once. Fibre Channel volumes support ownership management and SELinux
    relabeling.
    """

    fsType = Field(six.text_type)
    lun = RequiredField(int)
    readOnly = Field(bool)
    targetWWNs = ListField(six.text_type)


class ExecAction(Model):
    """
    ExecAction describes a 'run in container' action.
    """

    command = ListField(six.text_type)


class Probe(Model):
    """
    Probe describes a health check to be performed against a container to determine
    whether it is alive or ready to receive traffic.
    """

    _exec = Field(ExecAction)
    failureThreshold = Field(int)
    httpGet = Field(HTTPGetAction)
    initialDelaySeconds = Field(int)
    periodSeconds = Field(int)
    successThreshold = Field(int)
    tcpSocket = Field(TCPSocketAction)
    timeoutSeconds = Field(int)


class Handler(Model):
    """
    Handler defines a specific action that should be taken
    """

    _exec = Field(ExecAction)
    httpGet = Field(HTTPGetAction)
    tcpSocket = Field(TCPSocketAction)


class Lifecycle(Model):
    """
    Lifecycle describes actions that the management system should take in response
    to container lifecycle events. For the PostStart and PreStop lifecycle
    handlers, management of the container blocks until the action is complete,
    unless the container process fails, in which case the handler is aborted.
    """

    postStart = Field(Handler)
    preStop = Field(Handler)


class EventSource(Model):
    """
    EventSource contains information for an event.
    """

    component = Field(six.text_type)
    host = Field(six.text_type)


class Event(Model):
    """
    Event is a report of an event somewhere in the cluster.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/events"
        delete_url = "/api/v1/namespaces/{namespace}/events/{name}"
        get_url = "/api/v1/namespaces/{namespace}/events/{name}"
        list_all_url = "/api/v1/events"
        list_ns_url = "/api/v1/namespaces/{namespace}/events"
        update_url = "/api/v1/namespaces/{namespace}/events/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/events/{name}"
        watchlist_all_url = "/api/v1/watch/events"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/events"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Event")

    count = Field(int)
    firstTimestamp = Field(datetime.datetime)
    involvedObject = RequiredField(ObjectReference)
    lastTimestamp = Field(datetime.datetime)
    message = Field(six.text_type)
    metadata = RequiredField(ObjectMeta)
    reason = Field(six.text_type)
    source = Field(EventSource)
    type = Field(six.text_type)


class EventList(Model):
    """
    EventList is a list of events.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "EventList")

    items = ListField(Event)
    metadata = Field(ListMeta)


class EndpointPort(Model):
    """
    EndpointPort is a tuple that describes a single port.
    """

    name = Field(six.text_type)
    port = RequiredField(int)
    protocol = Field(six.text_type)


class EndpointSubset(Model):
    """
    EndpointSubset is a group of addresses with a common set of ports. The expanded
    set of endpoints is the Cartesian product of Addresses x Ports. For example,
    given:
      {
        Addresses: [{'ip': '10.10.1.1'}, {'ip': '10.10.2.2'}],
    Ports:     [{'name': 'a', 'port': 8675}, {'name': 'b', 'port': 309}]
      }
    The
    resulting set of endpoints can be viewed as:
        a: [ 10.10.1.1:8675,
    10.10.2.2:8675 ],
        b: [ 10.10.1.1:309, 10.10.2.2:309 ]
    """

    addresses = ListField(EndpointAddress)
    notReadyAddresses = ListField(EndpointAddress)
    ports = ListField(EndpointPort)


class Endpoints(Model):
    """
    Endpoints is a collection of endpoints that implement the actual service.
    Example:
      Name: 'mysvc',
      Subsets: [
        {
          Addresses: [{'ip':
    '10.10.1.1'}, {'ip': '10.10.2.2'}],
          Ports: [{'name': 'a', 'port': 8675},
    {'name': 'b', 'port': 309}]
        },
        {
          Addresses: [{'ip':
    '10.10.3.3'}],
          Ports: [{'name': 'a', 'port': 93}, {'name': 'b', 'port':
    76}]
        },
     ]
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/endpoints"
        delete_url = "/api/v1/namespaces/{namespace}/endpoints/{name}"
        get_url = "/api/v1/namespaces/{namespace}/endpoints/{name}"
        list_all_url = "/api/v1/endpoints"
        list_ns_url = "/api/v1/namespaces/{namespace}/endpoints"
        update_url = "/api/v1/namespaces/{namespace}/endpoints/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/endpoints/{name}"
        watchlist_all_url = "/api/v1/watch/endpoints"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/endpoints"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Endpoints")

    metadata = Field(ObjectMeta)
    subsets = ListField(EndpointSubset)


class EndpointsList(Model):
    """
    EndpointsList is a list of endpoints.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "EndpointsList")

    items = ListField(Endpoints)
    metadata = Field(ListMeta)


class EmptyDirVolumeSource(Model):
    """
    Represents an empty directory for a pod. Empty directory volumes support
    ownership management and SELinux relabeling.
    """

    medium = Field(six.text_type)


class DaemonEndpoint(Model):
    """
    DaemonEndpoint contains information about a single Daemon endpoint.
    """

    Port = RequiredField(int)


class NodeDaemonEndpoints(Model):
    """
    NodeDaemonEndpoints lists ports opened by daemons running on the Node.
    """

    kubeletEndpoint = Field(DaemonEndpoint)


class ContainerStateWaiting(Model):
    """
    ContainerStateWaiting is a waiting state of a container.
    """

    message = Field(six.text_type)
    reason = Field(six.text_type)


class ContainerStateTerminated(Model):
    """
    ContainerStateTerminated is a terminated state of a container.
    """

    containerID = Field(six.text_type)
    exitCode = RequiredField(int)
    finishedAt = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    signal = Field(int)
    startedAt = Field(datetime.datetime)


class ContainerStateRunning(Model):
    """
    ContainerStateRunning is a running state of a container.
    """

    startedAt = Field(datetime.datetime)


class ContainerState(Model):
    """
    ContainerState holds a possible state of container. Only one of its members may
    be specified. If none of them is specified, the default one is
    ContainerStateWaiting.
    """

    running = Field(ContainerStateRunning)
    terminated = Field(ContainerStateTerminated)
    waiting = Field(ContainerStateWaiting)


class ContainerStatus(Model):
    """
    ContainerStatus contains details for the current status of this container.
    """

    containerID = Field(six.text_type)
    image = RequiredField(six.text_type)
    imageID = RequiredField(six.text_type)
    lastState = Field(ContainerState)
    name = RequiredField(six.text_type)
    ready = RequiredField(bool)
    restartCount = RequiredField(int)
    state = Field(ContainerState)


class PodStatus(Model):
    """
    PodStatus represents information about the status of a pod. Status may trail
    the actual state of a system.
    """

    conditions = ListField(PodCondition)
    containerStatuses = ListField(ContainerStatus)
    hostIP = Field(six.text_type)
    initContainerStatuses = ListField(ContainerStatus)
    message = Field(six.text_type)
    phase = Field(six.text_type)
    podIP = Field(six.text_type)
    qosClass = Field(six.text_type)
    reason = Field(six.text_type)
    startTime = Field(datetime.datetime)


class ContainerPort(Model):
    """
    ContainerPort represents a network port in a single container.
    """

    containerPort = RequiredField(int)
    hostIP = Field(six.text_type)
    hostPort = Field(int)
    name = Field(six.text_type)
    protocol = Field(six.text_type)


class ContainerImage(Model):
    """
    Describe a container image
    """

    names = ListField(six.text_type)
    sizeBytes = Field(int)


class ConfigMapKeySelector(Model):
    """
    Selects a key from a ConfigMap.
    """

    key = RequiredField(six.text_type)
    name = Field(six.text_type)
    optional = Field(bool)


class EnvVarSource(Model):
    """
    EnvVarSource represents a source for the value of an EnvVar.
    """

    configMapKeyRef = Field(ConfigMapKeySelector)
    fieldRef = Field(ObjectFieldSelector)
    resourceFieldRef = Field(ResourceFieldSelector)
    secretKeyRef = Field(SecretKeySelector)


class EnvVar(Model):
    """
    EnvVar represents an environment variable present in a Container.
    """

    name = RequiredField(six.text_type)
    value = Field(six.text_type)
    valueFrom = Field(EnvVarSource)


class ConfigMapEnvSource(Model):
    """
    ConfigMapEnvSource selects a ConfigMap to populate the environment variables
    with.

    The contents of the target ConfigMap's Data field will represent the
    key-value pairs as environment variables.
    """

    name = Field(six.text_type)
    optional = Field(bool)


class EnvFromSource(Model):
    """
    EnvFromSource represents the source of a set of ConfigMaps
    """

    configMapRef = Field(ConfigMapEnvSource)
    prefix = Field(six.text_type)
    secretRef = Field(SecretEnvSource)


class ConfigMap(Model):
    """
    ConfigMap holds configuration data for pods to consume.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/configmaps"
        delete_url = "/api/v1/namespaces/{namespace}/configmaps/{name}"
        get_url = "/api/v1/namespaces/{namespace}/configmaps/{name}"
        list_all_url = "/api/v1/configmaps"
        list_ns_url = "/api/v1/namespaces/{namespace}/configmaps"
        update_url = "/api/v1/namespaces/{namespace}/configmaps/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/configmaps/{name}"
        watchlist_all_url = "/api/v1/watch/configmaps"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/configmaps"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ConfigMap")

    data = Field(dict)
    metadata = Field(ObjectMeta)


class ConfigMapList(Model):
    """
    ConfigMapList is a resource containing a list of ConfigMap objects.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ConfigMapList")

    items = ListField(ConfigMap)
    metadata = Field(ListMeta)


class ComponentCondition(Model):
    """
    Information about the condition of a component.
    """

    error = Field(six.text_type)
    message = Field(six.text_type)
    status = RequiredField(six.text_type)
    type = RequiredField(six.text_type)


class ComponentStatus(Model):
    """
    ComponentStatus (and ComponentStatusList) holds the cluster validation info.
    """
    class Meta:
        get_url = "/api/v1/componentstatuses/{name}"
        list_all_url = "/api/v1/componentstatuses"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ComponentStatus")

    conditions = ListField(ComponentCondition)
    metadata = Field(ObjectMeta)


class ComponentStatusList(Model):
    """
    Status of all the conditions for the component as a list of ComponentStatus
    objects.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ComponentStatusList")

    items = ListField(ComponentStatus)
    metadata = Field(ListMeta)


class CinderVolumeSource(Model):
    """
    Represents a cinder volume resource in Openstack. A Cinder volume must exist
    before mounting to a container. The volume must also be in the same region as
    the kubelet. Cinder volumes support ownership management and SELinux
    relabeling.
    """

    fsType = Field(six.text_type)
    readOnly = Field(bool)
    volumeID = RequiredField(six.text_type)


class Capabilities(Model):
    """
    Adds and removes POSIX capabilities from running containers.
    """

    add = ListField(six.text_type)
    drop = ListField(six.text_type)


class SecurityContext(Model):
    """
    SecurityContext holds security configuration that will be applied to a
    container. Some fields are present in both SecurityContext and
    PodSecurityContext.  When both are set, the values in SecurityContext take
    precedence.
    """

    capabilities = Field(Capabilities)
    privileged = Field(bool)
    readOnlyRootFilesystem = Field(bool)
    runAsNonRoot = Field(bool)
    runAsUser = Field(int)
    seLinuxOptions = Field(SELinuxOptions)


class Container(Model):
    """
    A single application container that you want to run within a pod.
    """

    args = ListField(six.text_type)
    command = ListField(six.text_type)
    env = ListField(EnvVar)
    envFrom = ListField(EnvFromSource)
    image = Field(six.text_type)
    imagePullPolicy = Field(six.text_type)
    lifecycle = Field(Lifecycle)
    livenessProbe = Field(Probe)
    name = RequiredField(six.text_type)
    ports = ListField(ContainerPort)
    readinessProbe = Field(Probe)
    resources = Field(ResourceRequirements)
    securityContext = Field(SecurityContext)
    stdin = Field(bool)
    stdinOnce = Field(bool)
    terminationMessagePath = Field(six.text_type)
    terminationMessagePolicy = Field(six.text_type)
    tty = Field(bool)
    volumeMounts = ListField(VolumeMount)
    workingDir = Field(six.text_type)


class AzureFileVolumeSource(Model):
    """
    AzureFile represents an Azure File Service mount on the host and bind mount to
    the pod.
    """

    readOnly = Field(bool)
    secretName = RequiredField(six.text_type)
    shareName = RequiredField(six.text_type)


class AzureDiskVolumeSource(Model):
    """
    AzureDisk represents an Azure Data Disk mount on the host and bind mount to the
    pod.
    """

    cachingMode = Field(six.text_type)
    diskName = RequiredField(six.text_type)
    diskURI = RequiredField(six.text_type)
    fsType = Field(six.text_type)
    readOnly = Field(bool)


class AttachedVolume(Model):
    """
    AttachedVolume describes a volume attached to a node
    """

    devicePath = RequiredField(six.text_type)
    name = RequiredField(six.text_type)


class NodeStatus(Model):
    """
    NodeStatus is information about the current status of a node.
    """

    addresses = ListField(NodeAddress)
    allocatable = Field(dict)
    capacity = Field(dict)
    conditions = ListField(NodeCondition)
    daemonEndpoints = Field(NodeDaemonEndpoints)
    images = ListField(ContainerImage)
    nodeInfo = Field(NodeSystemInfo)
    phase = Field(six.text_type)
    volumesAttached = ListField(AttachedVolume)
    volumesInUse = ListField(six.text_type)


class Node(Model):
    """
    Node is a worker node in Kubernetes. Each node will have a unique identifier in
    the cache (i.e. in etcd).
    """
    class Meta:
        create_url = "/api/v1/nodes"
        delete_url = "/api/v1/nodes/{name}"
        get_url = "/api/v1/nodes/{name}"
        list_all_url = "/api/v1/nodes"
        update_url = "/api/v1/nodes/{name}"
        watch_url = "/api/v1/watch/nodes/{name}"
        watchlist_all_url = "/api/v1/watch/nodes"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Node")

    metadata = Field(ObjectMeta)
    spec = Field(NodeSpec)
    status = ReadOnlyField(NodeStatus)


class NodeList(Model):
    """
    NodeList is the whole list of all Nodes which have been registered with master.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "NodeList")

    items = ListField(Node)
    metadata = Field(ListMeta)


class AWSElasticBlockStoreVolumeSource(Model):
    """
    Represents a Persistent Disk resource in AWS.

    An AWS EBS disk must exist
    before mounting to a container. The disk must also be in the same AWS zone as
    the kubelet. An AWS EBS disk can only be mounted as read/write once. AWS EBS
    volumes support ownership management and SELinux relabeling.
    """

    fsType = Field(six.text_type)
    partition = Field(int)
    readOnly = Field(bool)
    volumeID = RequiredField(six.text_type)


class Volume(Model):
    """
    Volume represents a named volume in a pod that may be accessed by any container
    in the pod.
    """

    awsElasticBlockStore = Field(AWSElasticBlockStoreVolumeSource)
    azureDisk = Field(AzureDiskVolumeSource)
    azureFile = Field(AzureFileVolumeSource)
    cephfs = Field(CephFSVolumeSource)
    cinder = Field(CinderVolumeSource)
    configMap = Field(ConfigMapVolumeSource)
    downwardAPI = Field(DownwardAPIVolumeSource)
    emptyDir = Field(EmptyDirVolumeSource)
    fc = Field(FCVolumeSource)
    flexVolume = Field(FlexVolumeSource)
    flocker = Field(FlockerVolumeSource)
    gcePersistentDisk = Field(GCEPersistentDiskVolumeSource)
    gitRepo = Field(GitRepoVolumeSource)
    glusterfs = Field(GlusterfsVolumeSource)
    hostPath = Field(HostPathVolumeSource)
    iscsi = Field(ISCSIVolumeSource)
    name = RequiredField(six.text_type)
    nfs = Field(NFSVolumeSource)
    persistentVolumeClaim = Field(PersistentVolumeClaimVolumeSource)
    photonPersistentDisk = Field(PhotonPersistentDiskVolumeSource)
    portworxVolume = Field(PortworxVolumeSource)
    projected = Field(ProjectedVolumeSource)
    quobyte = Field(QuobyteVolumeSource)
    rbd = Field(RBDVolumeSource)
    scaleIO = Field(ScaleIOVolumeSource)
    secret = Field(SecretVolumeSource)
    vsphereVolume = Field(VsphereVirtualDiskVolumeSource)


class PodSpec(Model):
    """
    PodSpec is a description of a pod.
    """

    activeDeadlineSeconds = Field(int)
    affinity = Field(Affinity)
    automountServiceAccountToken = Field(bool)
    containers = ListField(Container)
    dnsPolicy = Field(six.text_type)
    hostIPC = Field(bool)
    hostNetwork = Field(bool)
    hostPID = Field(bool)
    hostname = Field(six.text_type)
    imagePullSecrets = ListField(LocalObjectReference)
    initContainers = ListField(Container)
    nodeName = Field(six.text_type)
    nodeSelector = Field(dict)
    restartPolicy = Field(six.text_type)
    schedulerName = Field(six.text_type)
    securityContext = Field(PodSecurityContext)
    serviceAccount = Field(six.text_type)
    serviceAccountName = Field(six.text_type)
    subdomain = Field(six.text_type)
    terminationGracePeriodSeconds = Field(int)
    tolerations = ListField(Toleration)
    volumes = ListField(Volume)


class PodTemplateSpec(Model):
    """
    PodTemplateSpec describes the data a pod should have when created from a
    template
    """

    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)


class ReplicationControllerSpec(Model):
    """
    ReplicationControllerSpec is the specification of a replication controller.
    """

    minReadySeconds = Field(int)
    replicas = Field(int)
    selector = Field(dict)
    template = Field(PodTemplateSpec)


class ReplicationController(Model):
    """
    ReplicationController represents the configuration of a replication controller.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/replicationcontrollers"
        delete_url = "/api/v1/namespaces/{namespace}/replicationcontrollers/{name}"
        get_url = "/api/v1/namespaces/{namespace}/replicationcontrollers/{name}"
        list_all_url = "/api/v1/replicationcontrollers"
        list_ns_url = "/api/v1/namespaces/{namespace}/replicationcontrollers"
        update_url = "/api/v1/namespaces/{namespace}/replicationcontrollers/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/replicationcontrollers/{name}"
        watchlist_all_url = "/api/v1/watch/replicationcontrollers"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/replicationcontrollers"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ReplicationController")

    metadata = Field(ObjectMeta)
    spec = Field(ReplicationControllerSpec)
    status = ReadOnlyField(ReplicationControllerStatus)


class ReplicationControllerList(Model):
    """
    ReplicationControllerList is a collection of replication controllers.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "ReplicationControllerList")

    items = ListField(ReplicationController)
    metadata = Field(ListMeta)


class PodTemplate(Model):
    """
    PodTemplate describes a template for creating copies of a predefined pod.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/podtemplates"
        delete_url = "/api/v1/namespaces/{namespace}/podtemplates/{name}"
        get_url = "/api/v1/namespaces/{namespace}/podtemplates/{name}"
        list_all_url = "/api/v1/podtemplates"
        list_ns_url = "/api/v1/namespaces/{namespace}/podtemplates"
        update_url = "/api/v1/namespaces/{namespace}/podtemplates/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/podtemplates/{name}"
        watchlist_all_url = "/api/v1/watch/podtemplates"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/podtemplates"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PodTemplate")

    metadata = Field(ObjectMeta)
    template = Field(PodTemplateSpec)


class PodTemplateList(Model):
    """
    PodTemplateList is a list of PodTemplates.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PodTemplateList")

    items = ListField(PodTemplate)
    metadata = Field(ListMeta)


class Pod(Model):
    """
    Pod is a collection of containers that can run on a host. This resource is
    created by clients and scheduled onto hosts.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/pods"
        delete_url = "/api/v1/namespaces/{namespace}/pods/{name}"
        get_url = "/api/v1/namespaces/{namespace}/pods/{name}"
        list_all_url = "/api/v1/pods"
        list_ns_url = "/api/v1/namespaces/{namespace}/pods"
        update_url = "/api/v1/namespaces/{namespace}/pods/{name}"
        watch_url = "/api/v1/watch/namespaces/{namespace}/pods/{name}"
        watchlist_all_url = "/api/v1/watch/pods"
        watchlist_ns_url = "/api/v1/watch/namespaces/{namespace}/pods"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "Pod")

    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)
    status = ReadOnlyField(PodStatus)


class PodList(Model):
    """
    PodList is a list of Pods.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PodList")

    items = ListField(Pod)
    metadata = Field(ListMeta)


class PersistentVolumeSpec(Model):
    """
    PersistentVolumeSpec is the specification of a persistent volume.
    """

    accessModes = ListField(six.text_type)
    awsElasticBlockStore = Field(AWSElasticBlockStoreVolumeSource)
    azureDisk = Field(AzureDiskVolumeSource)
    azureFile = Field(AzureFileVolumeSource)
    capacity = Field(dict)
    cephfs = Field(CephFSVolumeSource)
    cinder = Field(CinderVolumeSource)
    claimRef = Field(ObjectReference)
    fc = Field(FCVolumeSource)
    flexVolume = Field(FlexVolumeSource)
    flocker = Field(FlockerVolumeSource)
    gcePersistentDisk = Field(GCEPersistentDiskVolumeSource)
    glusterfs = Field(GlusterfsVolumeSource)
    hostPath = Field(HostPathVolumeSource)
    iscsi = Field(ISCSIVolumeSource)
    nfs = Field(NFSVolumeSource)
    persistentVolumeReclaimPolicy = Field(six.text_type)
    photonPersistentDisk = Field(PhotonPersistentDiskVolumeSource)
    portworxVolume = Field(PortworxVolumeSource)
    quobyte = Field(QuobyteVolumeSource)
    rbd = Field(RBDVolumeSource)
    scaleIO = Field(ScaleIOVolumeSource)
    storageClassName = Field(six.text_type)
    vsphereVolume = Field(VsphereVirtualDiskVolumeSource)


class PersistentVolume(Model):
    """
    PersistentVolume (PV) is a storage resource provisioned by an administrator. It
    is analogous to a node. More info: http://kubernetes.io/docs/user-guide
    /persistent-volumes
    """
    class Meta:
        create_url = "/api/v1/persistentvolumes"
        delete_url = "/api/v1/persistentvolumes/{name}"
        get_url = "/api/v1/persistentvolumes/{name}"
        list_all_url = "/api/v1/persistentvolumes"
        update_url = "/api/v1/persistentvolumes/{name}"
        watch_url = "/api/v1/watch/persistentvolumes/{name}"
        watchlist_all_url = "/api/v1/watch/persistentvolumes"
    
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PersistentVolume")

    metadata = Field(ObjectMeta)
    spec = Field(PersistentVolumeSpec)
    status = ReadOnlyField(PersistentVolumeStatus)


class PersistentVolumeList(Model):
    """
    PersistentVolumeList is a list of PersistentVolume items.
    """
    apiVersion = Field(six.text_type, "v1")
    kind = Field(six.text_type, "PersistentVolumeList")

    items = ListField(PersistentVolume)
    metadata = Field(ListMeta)

