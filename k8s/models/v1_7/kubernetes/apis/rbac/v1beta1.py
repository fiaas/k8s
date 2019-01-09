#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class Subject(Model):
    """
    Subject contains a reference to the object or user identities a role binding
    applies to.  This can either hold a direct API object reference, or a value for
    non-objects such as user and group names.
    """

    apiGroup = Field(six.text_type)
    name = RequiredField(six.text_type)
    namespace = Field(six.text_type)


class RoleRef(Model):
    """
    RoleRef contains information that points to the role being used
    """

    apiGroup = RequiredField(six.text_type)
    name = RequiredField(six.text_type)


class RoleBinding(Model):
    """
    RoleBinding references a role, but does not contain it.  It can reference a
    Role in the same namespace or a ClusterRole in the global namespace. It adds
    who information via Subjects and namespace information by which namespace it
    exists in.  RoleBindings in a given namespace only have effect in that
    namespace.
    """
    class Meta:
        create_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/rolebindings"
        delete_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/rolebindings/{name}"
        get_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/rolebindings/{name}"
        list_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/rolebindings"
        list_ns_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/rolebindings"
        update_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/rolebindings/{name}"
        watch_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/namespaces/{namespace}/rolebindings/{name}"
        watchlist_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/rolebindings"
        watchlist_ns_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/namespaces/{namespace}/rolebindings"
    
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "RoleBinding")

    metadata = Field(ObjectMeta)
    roleRef = RequiredField(RoleRef)
    subjects = ListField(Subject)


class RoleBindingList(Model):
    """
    RoleBindingList is a collection of RoleBindings
    """
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "RoleBindingList")

    items = ListField(RoleBinding)
    metadata = Field(ListMeta)


class ClusterRoleBinding(Model):
    """
    ClusterRoleBinding references a ClusterRole, but not contain it.  It can
    reference a ClusterRole in the global namespace, and adds who information via
    Subject.
    """
    class Meta:
        create_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings"
        delete_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings/{name}"
        get_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings/{name}"
        list_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings"
        update_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings/{name}"
        watch_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/clusterrolebindings/{name}"
        watchlist_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/clusterrolebindings"
    
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "ClusterRoleBinding")

    metadata = Field(ObjectMeta)
    roleRef = RequiredField(RoleRef)
    subjects = ListField(Subject)


class ClusterRoleBindingList(Model):
    """
    ClusterRoleBindingList is a collection of ClusterRoleBindings
    """
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "ClusterRoleBindingList")

    items = ListField(ClusterRoleBinding)
    metadata = Field(ListMeta)


class PolicyRule(Model):
    """
    PolicyRule holds information that describes a policy rule, but does not contain
    information about who the rule applies to or which namespace the rule applies
    to.
    """

    apiGroups = ListField(six.text_type)
    nonResourceURLs = ListField(six.text_type)
    resourceNames = ListField(six.text_type)
    resources = ListField(six.text_type)
    verbs = ListField(six.text_type)


class Role(Model):
    """
    Role is a namespaced, logical grouping of PolicyRules that can be referenced as
    a unit by a RoleBinding.
    """
    class Meta:
        create_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/roles"
        delete_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/roles/{name}"
        get_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/roles/{name}"
        list_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/roles"
        list_ns_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/roles"
        update_url = "/apis/rbac.authorization.k8s.io/v1beta1/namespaces/{namespace}/roles/{name}"
        watch_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/namespaces/{namespace}/roles/{name}"
        watchlist_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/roles"
        watchlist_ns_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/namespaces/{namespace}/roles"
    
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "Role")

    metadata = Field(ObjectMeta)
    rules = ListField(PolicyRule)


class RoleList(Model):
    """
    RoleList is a collection of Roles
    """
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "RoleList")

    items = ListField(Role)
    metadata = Field(ListMeta)


class ClusterRole(Model):
    """
    ClusterRole is a cluster level, logical grouping of PolicyRules that can be
    referenced as a unit by a RoleBinding or ClusterRoleBinding.
    """
    class Meta:
        create_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterroles"
        delete_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterroles/{name}"
        get_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterroles/{name}"
        list_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterroles"
        update_url = "/apis/rbac.authorization.k8s.io/v1beta1/clusterroles/{name}"
        watch_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/clusterroles/{name}"
        watchlist_all_url = "/apis/rbac.authorization.k8s.io/v1beta1/watch/clusterroles"
    
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "ClusterRole")

    metadata = Field(ObjectMeta)
    rules = ListField(PolicyRule)


class ClusterRoleList(Model):
    """
    ClusterRoleList is a collection of ClusterRoles
    """
    apiVersion = Field(six.text_type, "rbac.authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "ClusterRoleList")

    items = ListField(ClusterRole)
    metadata = Field(ListMeta)

