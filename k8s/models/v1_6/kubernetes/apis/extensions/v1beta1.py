#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, ReadOnlyField, RequiredField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta
from k8s.models.v1_6.kubernetes.api.v1 import LoadBalancerStatus, PodTemplateSpec, SELinuxOptions


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class APIVersion(Model):
    """
    An APIVersion represents a single concrete version of an object model.
    """

    name = Field(six.text_type)


class ThirdPartyResource(Model):
    """
    A ThirdPartyResource is a generic representation of a resource, it is used by
    add-ons and plugins to add new resource types to the API.  It consists of one
    or more Versions of the api.
    """
    class Meta:
        create_url = "/apis/extensions/v1beta1/thirdpartyresources"
        delete_url = "/apis/extensions/v1beta1/thirdpartyresources/{name}"
        get_url = "/apis/extensions/v1beta1/thirdpartyresources/{name}"
        list_all_url = "/apis/extensions/v1beta1/thirdpartyresources"
        update_url = "/apis/extensions/v1beta1/thirdpartyresources/{name}"
        watch_url = "/apis/extensions/v1beta1/watch/thirdpartyresources/{name}"
        watchlist_all_url = "/apis/extensions/v1beta1/watch/thirdpartyresources"
    
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "ThirdPartyResource")

    description = Field(six.text_type)
    metadata = Field(ObjectMeta)
    versions = ListField(APIVersion)


class ThirdPartyResourceList(Model):
    """
    ThirdPartyResourceList is a list of ThirdPartyResources.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "ThirdPartyResourceList")

    items = ListField(ThirdPartyResource)
    metadata = Field(ListMeta)


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


class IDRange(Model):
    """
    ID Range provides a min/max of an allowed range of IDs.
    """

    max = RequiredField(int)
    min = RequiredField(int)


class RunAsUserStrategyOptions(Model):
    """
    Run A sUser Strategy Options defines the strategy type and any options used to
    create the strategy.
    """

    ranges = ListField(IDRange)
    rule = RequiredField(six.text_type)


class SupplementalGroupsStrategyOptions(Model):
    """
    SupplementalGroupsStrategyOptions defines the strategy type and options used to
    create the strategy.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


class FSGroupStrategyOptions(Model):
    """
    FSGroupStrategyOptions defines the strategy type and options used to create the
    strategy.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


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
    conditions = ListField(DeploymentCondition)
    observedGeneration = Field(int)
    readyReplicas = Field(int)
    replicas = Field(int)
    unavailableReplicas = Field(int)
    updatedReplicas = Field(int)


class SELinuxStrategyOptions(Model):
    """
    SELinux  Strategy Options defines the strategy type and any options used to
    create the strategy.
    """

    rule = RequiredField(six.text_type)
    seLinuxOptions = Field(SELinuxOptions)


class NetworkPolicyPort(Model):
    """
    
    """

    port = Field(six.text_type, alt_type=int)
    protocol = Field(six.text_type)


class DaemonSetStatus(Model):
    """
    DaemonSetStatus represents the current status of a daemon set.
    """

    currentNumberScheduled = RequiredField(int)
    desiredNumberScheduled = RequiredField(int)
    numberAvailable = Field(int)
    numberMisscheduled = RequiredField(int)
    numberReady = RequiredField(int)
    numberUnavailable = Field(int)
    observedGeneration = Field(int)
    updatedNumberScheduled = Field(int)


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
    selector = Field(LabelSelector)
    template = RequiredField(PodTemplateSpec)
    templateGeneration = Field(int)
    updateStrategy = Field(DaemonSetUpdateStrategy)


class DaemonSet(Model):
    """
    DaemonSet represents the configuration of a daemon set.
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


class ReplicaSetSpec(Model):
    """
    ReplicaSetSpec is the specification of a ReplicaSet.
    """

    minReadySeconds = Field(int)
    replicas = Field(int)
    selector = Field(LabelSelector)
    template = Field(PodTemplateSpec)


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


class RollbackConfig(Model):
    """
    
    """

    revision = Field(int)


class DeploymentRollback(Model):
    """
    DeploymentRollback stores the information required to rollback a deployment.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "DeploymentRollback")

    name = RequiredField(six.text_type)
    rollbackTo = RequiredField(RollbackConfig)
    updatedAnnotations = Field(dict)


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


class ScaleSpec(Model):
    """
    describes the attributes of a scale subresource
    """

    replicas = Field(int)


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


class HostPortRange(Model):
    """
    Host Port Range defines a range of host ports that will be enabled by a policy
    for pods to use.  It requires both the start and end to be defined.
    """

    max = RequiredField(int)
    min = RequiredField(int)


class PodSecurityPolicySpec(Model):
    """
    Pod Security Policy Spec defines the policy enforced.
    """

    allowedCapabilities = ListField(six.text_type)
    defaultAddCapabilities = ListField(six.text_type)
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
    Pod Security Policy governs the ability to make requests that affect the
    Security Context that will be applied to a pod and container.
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
    Pod Security Policy List is a list of PodSecurityPolicy objects.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "PodSecurityPolicyList")

    items = ListField(PodSecurityPolicy)
    metadata = Field(ListMeta)


class NetworkPolicyPeer(Model):
    """
    
    """

    namespaceSelector = Field(LabelSelector)
    podSelector = Field(LabelSelector)


class NetworkPolicyIngressRule(Model):
    """
    This NetworkPolicyIngressRule matches traffic if and only if the traffic
    matches both ports AND from.
    """

    _from = ListField(NetworkPolicyPeer)
    ports = ListField(NetworkPolicyPort)


class NetworkPolicySpec(Model):
    """
    
    """

    ingress = ListField(NetworkPolicyIngressRule)
    podSelector = RequiredField(LabelSelector)


class NetworkPolicy(Model):
    """
    
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
    Network Policy List is a list of NetworkPolicy objects.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "NetworkPolicyList")

    items = ListField(NetworkPolicy)
    metadata = Field(ListMeta)


class ScaleStatus(Model):
    """
    represents the current status of a scale subresource.
    """

    replicas = RequiredField(int)
    selector = Field(dict)
    targetSelector = Field(six.text_type)


class Scale(Model):
    """
    represents a scaling request for a resource.
    """
    apiVersion = Field(six.text_type, "extensions/v1beta1")
    kind = Field(six.text_type, "Scale")

    metadata = Field(ObjectMeta)
    spec = Field(ScaleSpec)
    status = ReadOnlyField(ScaleStatus)


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
    ReplicaSet represents the configuration of a ReplicaSet.
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

