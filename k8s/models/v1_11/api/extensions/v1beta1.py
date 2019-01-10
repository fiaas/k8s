#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_11.api.core.v1 import LoadBalancerStatus, PodTemplateSpec, SELinuxOptions
from k8s.models.v1_11.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class ScaleStatus(Model):
    """
    represents the current status of a scale subresource.
    """

    replicas = RequiredField(int)
    selector = Field(dict)
    targetSelector = Field(six.text_type)


class ScaleSpec(Model):
    """
    describes the attributes of a scale subresource
    """

    replicas = Field(int)


class Scale(Model):
    """
    represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = ReadOnlyField(ScaleStatus)


class SELinuxStrategyOptions(Model):
    """
    SELinuxStrategyOptions defines the strategy type and any options used to create
    the strategy. Deprecated: use SELinuxStrategyOptions from policy API Group
    instead.
    """

    rule = RequiredField(six.text_type)
    seLinuxOptions = Field(SELinuxOptions)


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


class RollingUpdateDaemonSet(Model):
    """
    Spec to control the desired behavior of daemon set rolling update.
    """

    maxUnavailable = Field(six.text_type, alt_type=int)


class DaemonSetUpdateStrategy(Model):
    """
    
    """

    rollingUpdate = Field(RollingUpdateDaemonSet)
    type = Field(six.text_type)


class DaemonSetSpec(Model):
    """
    DaemonSetSpec is the specification of a daemon set.
    """

    minReadySeconds = Field(int)
    revisionHistoryLimit = Field(int)
    selector = Field(LabelSelector)
    template = RequiredField(PodTemplateSpec)
    templateGeneration = Field(int)
    updateStrategy = Field(DaemonSetUpdateStrategy)


class RollbackConfig(Model):
    """
    DEPRECATED.
    """

    revision = Field(int)


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


class DeploymentRollback(Model):
    """
    DEPRECATED. DeploymentRollback stores the information required to rollback a
    deployment.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "DeploymentRollback")

    name = RequiredField(six.text_type)
    rollbackTo = RequiredField(RollbackConfig)
    updatedAnnotations = Field(dict)


class ReplicaSetSpec(Model):
    """
    ReplicaSetSpec is the specification of a ReplicaSet.
    """

    minReadySeconds = Field(int)
    replicas = Field(int)
    selector = Field(LabelSelector)
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
    apps/v1beta2/ReplicaSet. See the release notes for more information. ReplicaSet
    ensures that a specified number of pod replicas are running at any given time.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/namespaces/{namespace}/replicasets"
        delete_url = "/apis/extensions/v1beta1/namespaces/{namespace}/replicasets/{name}"
        get_url = "/apis/extensions/v1beta1/namespaces/{namespace}/replicasets/{name}"
        list_all_url = "/apis/extensions/v1beta1/replicasets"
        list_ns_url = "/apis/extensions/v1beta1/namespaces/{namespace}/replicasets"
        update_url = "/apis/extensions/v1beta1/namespaces/{namespace}/replicasets/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/replicasets/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/replicasets"
        watchlist_ns_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/replicasets"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "ReplicaSet")

    metadata = Field(ObjectMeta)
    spec = Field(ReplicaSetSpec)
    status = ReadOnlyField(ReplicaSetStatus)


class ReplicaSetList(Model):
    """
    ReplicaSetList is a collection of ReplicaSets.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "ReplicaSetList")

    items = ListField(ReplicaSet)
    metadata = Field(ListMeta)


class NetworkPolicyPort(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicyPort is deprecated by
    networking/v1/NetworkPolicyPort.
    """

    port = Field(six.text_type, alt_type=int)
    protocol = Field(six.text_type)


class IngressTLS(Model):
    """
    IngressTLS describes the transport layer security associated with an Ingress.
    """

    hosts = ListField(six.text_type)
    secretName = Field(six.text_type)


class IngressStatus(Model):
    """
    IngressStatus describe the current state of the Ingress.
    """

    loadBalancer = Field(LoadBalancerStatus)


class IngressBackend(Model):
    """
    IngressBackend describes all endpoints for a given service and port.
    """

    serviceName = RequiredField(six.text_type)
    servicePort = RequiredField(six.text_type, alt_type=int)


class HTTPIngressPath(Model):
    """
    HTTPIngressPath associates a path regex with a backend. Incoming urls matching
    the path are forwarded to the backend.
    """

    backend = RequiredField(IngressBackend)
    path = Field(six.text_type)


class HTTPIngressRuleValue(Model):
    """
    HTTPIngressRuleValue is a list of http selectors pointing to backends. In the
    example: http://<host>/<path>?<searchpart> -> backend where where parts of the
    url correspond to RFC 3986, this resource will be used to match against
    everything after the last '/' and before the first '?' or '#'.
    """

    paths = ListField(HTTPIngressPath)


class IngressRule(Model):
    """
    IngressRule represents the rules mapping the paths under a specified host to
    the related backend services. Incoming requests are first evaluated for a host
    match, then routed to the backend associated with the matching
    IngressRuleValue.
    """

    host = Field(six.text_type)
    http = Field(HTTPIngressRuleValue)


class IngressSpec(Model):
    """
    IngressSpec describes the Ingress the user wishes to exist.
    """

    backend = Field(IngressBackend)
    rules = ListField(IngressRule)
    tls = ListField(IngressTLS)


class Ingress(Model):
    """
    Ingress is a collection of rules that allow inbound connections to reach the
    endpoints defined by a backend. An Ingress can be configured to give services
    externally-reachable urls, load balance traffic, terminate SSL, offer name
    based virtual hosting etc.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses"
        delete_url = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}"
        get_url = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}"
        list_all_url = "/apis/extensions/v1beta1/ingresses"
        list_ns_url = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses"
        update_url = "/apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/ingresses/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/ingresses"
        watchlist_ns_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/ingresses"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "Ingress")

    metadata = Field(ObjectMeta)
    spec = Field(IngressSpec)
    status = Field(IngressStatus)


class IngressList(Model):
    """
    IngressList is a collection of Ingress.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "IngressList")

    items = ListField(Ingress)
    metadata = Field(ListMeta)


class IPBlock(Model):
    """
    DEPRECATED 1.9 - This group version of IPBlock is deprecated by
    networking/v1/IPBlock. IPBlock describes a particular CIDR (Ex.
    '192.168.1.1/24') that is allowed to the pods matched by a NetworkPolicySpec's
    podSelector. The except entry describes CIDRs that should not be included
    within this rule.
    """

    _except = ListField(six.text_type)
    cidr = RequiredField(six.text_type)


class NetworkPolicyPeer(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicyPeer is deprecated by
    networking/v1/NetworkPolicyPeer.
    """

    ipBlock = Field(IPBlock)
    namespaceSelector = Field(LabelSelector)
    podSelector = Field(LabelSelector)


class NetworkPolicyIngressRule(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicyIngressRule is deprecated
    by networking/v1/NetworkPolicyIngressRule. This NetworkPolicyIngressRule
    matches traffic if and only if the traffic matches both ports AND from.
    """

    _from = ListField(NetworkPolicyPeer)
    ports = ListField(NetworkPolicyPort)


class NetworkPolicyEgressRule(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicyEgressRule is deprecated by
    networking/v1/NetworkPolicyEgressRule. NetworkPolicyEgressRule describes a
    particular set of traffic that is allowed out of pods matched by a
    NetworkPolicySpec's podSelector. The traffic must match both ports and to. This
    type is beta-level in 1.8
    """

    ports = ListField(NetworkPolicyPort)
    to = ListField(NetworkPolicyPeer)


class NetworkPolicySpec(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicySpec is deprecated by
    networking/v1/NetworkPolicySpec.
    """

    egress = ListField(NetworkPolicyEgressRule)
    ingress = ListField(NetworkPolicyIngressRule)
    podSelector = RequiredField(LabelSelector)
    policyTypes = ListField(six.text_type)


class NetworkPolicy(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicy is deprecated by
    networking/v1/NetworkPolicy. NetworkPolicy describes what network traffic is
    allowed for a set of Pods
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/namespaces/{namespace}/networkpolicies"
        delete_url = "/apis/extensions/v1beta1/namespaces/{namespace}/networkpolicies/{name}"
        get_url = "/apis/extensions/v1beta1/namespaces/{namespace}/networkpolicies/{name}"
        list_all_url = "/apis/extensions/v1beta1/networkpolicies"
        list_ns_url = "/apis/extensions/v1beta1/namespaces/{namespace}/networkpolicies"
        update_url = "/apis/extensions/v1beta1/namespaces/{namespace}/networkpolicies/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/networkpolicies/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/networkpolicies"
        watchlist_ns_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/networkpolicies"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "NetworkPolicy")

    metadata = Field(ObjectMeta)
    spec = Field(NetworkPolicySpec)


class NetworkPolicyList(Model):
    """
    DEPRECATED 1.9 - This group version of NetworkPolicyList is deprecated by
    networking/v1/NetworkPolicyList. Network Policy List is a list of NetworkPolicy
    objects.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "NetworkPolicyList")

    items = ListField(NetworkPolicy)
    metadata = Field(ListMeta)


class IDRange(Model):
    """
    IDRange provides a min/max of an allowed range of IDs. Deprecated: use IDRange
    from policy API Group instead.
    """

    max = RequiredField(int)
    min = RequiredField(int)


class SupplementalGroupsStrategyOptions(Model):
    """
    SupplementalGroupsStrategyOptions defines the strategy type and options used to
    create the strategy. Deprecated: use SupplementalGroupsStrategyOptions from
    policy API Group instead.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


class RunAsUserStrategyOptions(Model):
    """
    RunAsUserStrategyOptions defines the strategy type and any options used to
    create the strategy. Deprecated: use RunAsUserStrategyOptions from policy API
    Group instead.
    """

    ranges = ListField(IDRange)
    rule = RequiredField(six.text_type)


class FSGroupStrategyOptions(Model):
    """
    FSGroupStrategyOptions defines the strategy type and options used to create the
    strategy. Deprecated: use FSGroupStrategyOptions from policy API Group instead.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


class HostPortRange(Model):
    """
    HostPortRange defines a range of host ports that will be enabled by a policy
    for pods to use.  It requires both the start and end to be defined. Deprecated:
    use HostPortRange from policy API Group instead.
    """

    max = RequiredField(int)
    min = RequiredField(int)


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
    apps/v1beta2/Deployment. See the release notes for more information. Deployment
    enables declarative updates for Pods and ReplicaSets.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/namespaces/{namespace}/deployments"
        delete_url = "/apis/extensions/v1beta1/namespaces/{namespace}/deployments/{name}"
        get_url = "/apis/extensions/v1beta1/namespaces/{namespace}/deployments/{name}"
        list_all_url = "/apis/extensions/v1beta1/deployments"
        list_ns_url = "/apis/extensions/v1beta1/namespaces/{namespace}/deployments"
        update_url = "/apis/extensions/v1beta1/namespaces/{namespace}/deployments/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/deployments/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/deployments"
        watchlist_ns_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/deployments"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "Deployment")

    metadata = Field(ObjectMeta)
    spec = Field(DeploymentSpec)
    status = Field(DeploymentStatus)


class DeploymentList(Model):
    """
    DeploymentList is a list of Deployments.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
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
    apps/v1beta2/DaemonSet. See the release notes for more information. DaemonSet
    represents the configuration of a daemon set.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/namespaces/{namespace}/daemonsets"
        delete_url = "/apis/extensions/v1beta1/namespaces/{namespace}/daemonsets/{name}"
        get_url = "/apis/extensions/v1beta1/namespaces/{namespace}/daemonsets/{name}"
        list_all_url = "/apis/extensions/v1beta1/daemonsets"
        list_ns_url = "/apis/extensions/v1beta1/namespaces/{namespace}/daemonsets"
        update_url = "/apis/extensions/v1beta1/namespaces/{namespace}/daemonsets/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/daemonsets/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/daemonsets"
        watchlist_ns_url = "/apis/extensions/v1beta1/watch/namespaces/{namespace}/daemonsets"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "DaemonSet")

    metadata = Field(ObjectMeta)
    spec = Field(DaemonSetSpec)
    status = ReadOnlyField(DaemonSetStatus)


class DaemonSetList(Model):
    """
    DaemonSetList is a collection of daemon sets.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "DaemonSetList")

    items = ListField(DaemonSet)
    metadata = Field(ListMeta)


class AllowedHostPath(Model):
    """
    AllowedHostPath defines the host volume conditions that will be enabled by a
    policy for pods to use. It requires the path prefix to be defined. Deprecated:
    use AllowedHostPath from policy API Group instead.
    """

    pathPrefix = Field(six.text_type)
    readOnly = Field(bool)


class AllowedFlexVolume(Model):
    """
    AllowedFlexVolume represents a single Flexvolume that is allowed to be used.
    Deprecated: use AllowedFlexVolume from policy API Group instead.
    """

    driver = RequiredField(six.text_type)


class PodSecurityPolicySpec(Model):
    """
    PodSecurityPolicySpec defines the policy enforced. Deprecated: use
    PodSecurityPolicySpec from policy API Group instead.
    """

    allowPrivilegeEscalation = Field(bool)
    allowedCapabilities = ListField(six.text_type)
    allowedFlexVolumes = ListField(AllowedFlexVolume)
    allowedHostPaths = ListField(AllowedHostPath)
    allowedUnsafeSysctls = ListField(six.text_type)
    defaultAddCapabilities = ListField(six.text_type)
    defaultAllowPrivilegeEscalation = Field(bool)
    forbiddenSysctls = ListField(six.text_type)
    fsGroup = RequiredField(FSGroupStrategyOptions)
    hostIPC = Field(bool)
    hostNetwork = Field(bool)
    hostPID = Field(bool)
    hostPorts = ListField(HostPortRange)
    privileged = Field(bool)
    readOnlyRootFilesystem = Field(bool)
    requiredDropCapabilities = ListField(six.text_type)
    runAsUser = RequiredField(RunAsUserStrategyOptions)
    seLinux = RequiredField(SELinuxStrategyOptions)
    supplementalGroups = RequiredField(SupplementalGroupsStrategyOptions)
    volumes = ListField(six.text_type)


class PodSecurityPolicy(Model):
    """
    PodSecurityPolicy governs the ability to make requests that affect the Security
    Context that will be applied to a pod and container. Deprecated: use
    PodSecurityPolicy from policy API Group instead.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/podsecuritypolicies"
        delete_url = "/apis/extensions/v1beta1/podsecuritypolicies/{name}"
        get_url = "/apis/extensions/v1beta1/podsecuritypolicies/{name}"
        list_all_url = "/apis/extensions/v1beta1/podsecuritypolicies"
        update_url = "/apis/extensions/v1beta1/podsecuritypolicies/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/podsecuritypolicies/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/podsecuritypolicies"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "PodSecurityPolicy")

    metadata = Field(ObjectMeta)
    spec = Field(PodSecurityPolicySpec)


class PodSecurityPolicyList(Model):
    """
    PodSecurityPolicyList is a list of PodSecurityPolicy objects. Deprecated: use
    PodSecurityPolicyList from policy API Group instead.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "PodSecurityPolicyList")

    items = ListField(PodSecurityPolicy)
    metadata = Field(ListMeta)

