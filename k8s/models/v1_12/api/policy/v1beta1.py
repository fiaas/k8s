#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_12.api.core.v1 import SELinuxOptions
from k8s.models.v1_12.apimachinery.apis.meta.v1 import DeleteOptions, LabelSelector, ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class SELinuxStrategyOptions(Model):
    """
    SELinuxStrategyOptions defines the strategy type and any options used to create
    the strategy.
    """

    rule = RequiredField(six.text_type)
    seLinuxOptions = Field(SELinuxOptions)


class PodDisruptionBudgetStatus(Model):
    """
    PodDisruptionBudgetStatus represents information about the status of a
    PodDisruptionBudget. Status may trail the actual state of a system.
    """

    currentHealthy = RequiredField(int)
    desiredHealthy = RequiredField(int)
    disruptedPods = Field(dict)
    disruptionsAllowed = RequiredField(int)
    expectedPods = RequiredField(int)
    observedGeneration = Field(int)


class PodDisruptionBudgetSpec(Model):
    """
    PodDisruptionBudgetSpec is a description of a PodDisruptionBudget.
    """

    maxUnavailable = Field(six.text_type, alt_type=int)
    minAvailable = Field(six.text_type, alt_type=int)
    selector = Field(LabelSelector)


class PodDisruptionBudget(Model):
    """
    PodDisruptionBudget is an object to define the max disruption that can be
    caused to a collection of pods
    """
    class Meta:
        create_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets"
        delete_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        get_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        list_all_url = "/apis/policy/v1beta1/poddisruptionbudgets"
        list_ns_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets"
        update_url = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"
        watch_url = "/apis/policy/v1beta1/watch/namespaces/{namespace}/poddisruptionbudgets/{name}"
        watchlist_all_url = "/apis/policy/v1beta1/watch/poddisruptionbudgets"
        watchlist_ns_url = "/apis/policy/v1beta1/watch/namespaces/{namespace}/poddisruptionbudgets"
    
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodDisruptionBudget")

    metadata = Field(ObjectMeta)
    spec = Field(PodDisruptionBudgetSpec)
    status = Field(PodDisruptionBudgetStatus)


class PodDisruptionBudgetList(Model):
    """
    PodDisruptionBudgetList is a collection of PodDisruptionBudgets.
    """
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodDisruptionBudgetList")

    items = ListField(PodDisruptionBudget)
    metadata = Field(ListMeta)


class IDRange(Model):
    """
    IDRange provides a min/max of an allowed range of IDs.
    """

    max = RequiredField(int)
    min = RequiredField(int)


class SupplementalGroupsStrategyOptions(Model):
    """
    SupplementalGroupsStrategyOptions defines the strategy type and options used to
    create the strategy.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


class RunAsUserStrategyOptions(Model):
    """
    RunAsUserStrategyOptions defines the strategy type and any options used to
    create the strategy.
    """

    ranges = ListField(IDRange)
    rule = RequiredField(six.text_type)


class FSGroupStrategyOptions(Model):
    """
    FSGroupStrategyOptions defines the strategy type and options used to create the
    strategy.
    """

    ranges = ListField(IDRange)
    rule = Field(six.text_type)


class HostPortRange(Model):
    """
    HostPortRange defines a range of host ports that will be enabled by a policy
    for pods to use.  It requires both the start and end to be defined.
    """

    max = RequiredField(int)
    min = RequiredField(int)


class Eviction(Model):
    """
    Eviction evicts a pod from its node subject to certain policies and safety
    constraints. This is a subresource of Pod.  A request to cause such an eviction
    is created by POSTing to .../pods/<pod name>/evictions.
    """
    class Meta:
        create_url = "/api/v1/namespaces/{namespace}/pods/{name}/eviction"
    
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "Eviction")

    deleteOptions = Field(DeleteOptions)
    metadata = Field(ObjectMeta)


class AllowedHostPath(Model):
    """
    AllowedHostPath defines the host volume conditions that will be enabled by a
    policy for pods to use. It requires the path prefix to be defined.
    """

    pathPrefix = Field(six.text_type)
    readOnly = Field(bool)


class AllowedFlexVolume(Model):
    """
    AllowedFlexVolume represents a single Flexvolume that is allowed to be used.
    """

    driver = RequiredField(six.text_type)


class PodSecurityPolicySpec(Model):
    """
    PodSecurityPolicySpec defines the policy enforced.
    """

    allowPrivilegeEscalation = Field(bool)
    allowedCapabilities = ListField(six.text_type)
    allowedFlexVolumes = ListField(AllowedFlexVolume)
    allowedHostPaths = ListField(AllowedHostPath)
    allowedProcMountTypes = ListField(six.text_type)
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
    Context that will be applied to a pod and container.
    """
    class Meta:
        create_url = "/apis/policy/v1beta1/podsecuritypolicies"
        delete_url = "/apis/policy/v1beta1/podsecuritypolicies/{name}"
        get_url = "/apis/policy/v1beta1/podsecuritypolicies/{name}"
        list_all_url = "/apis/policy/v1beta1/podsecuritypolicies"
        update_url = "/apis/policy/v1beta1/podsecuritypolicies/{name}"
        watch_url = "/apis/policy/v1beta1/watch/podsecuritypolicies/{name}"
        watchlist_all_url = "/apis/policy/v1beta1/watch/podsecuritypolicies"
    
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodSecurityPolicy")

    metadata = Field(ObjectMeta)
    spec = Field(PodSecurityPolicySpec)


class PodSecurityPolicyList(Model):
    """
    PodSecurityPolicyList is a list of PodSecurityPolicy objects.
    """
    apiVersion = Field(six.text_type, "policy/v1beta1")
    kind = Field(six.text_type, "PodSecurityPolicyList")

    items = ListField(PodSecurityPolicy)
    metadata = Field(ListMeta)

