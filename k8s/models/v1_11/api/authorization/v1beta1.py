#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_11.apimachinery.apis.meta.v1 import ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class SubjectAccessReviewStatus(Model):
    """
    SubjectAccessReviewStatus
    """

    allowed = RequiredField(bool)
    denied = Field(bool)
    evaluationError = Field(six.text_type)
    reason = Field(six.text_type)


class SelfSubjectRulesReviewSpec(Model):
    """
    
    """

    namespace = Field(six.text_type)


class ResourceRule(Model):
    """
    ResourceRule is the list of actions the subject is allowed to perform on
    resources. The list ordering isn't significant, may contain duplicates, and
    possibly be incomplete.
    """

    apiGroups = ListField(six.text_type)
    resourceNames = ListField(six.text_type)
    resources = ListField(six.text_type)
    verbs = ListField(six.text_type)


class ResourceAttributes(Model):
    """
    ResourceAttributes includes the authorization attributes available for resource
    requests to the Authorizer interface
    """

    group = Field(six.text_type)
    name = Field(six.text_type)
    namespace = Field(six.text_type)
    resource = Field(six.text_type)
    subresource = Field(six.text_type)
    verb = Field(six.text_type)
    version = Field(six.text_type)


class NonResourceRule(Model):
    """
    NonResourceRule holds information that describes a rule for the non-resource
    """

    nonResourceURLs = ListField(six.text_type)
    verbs = ListField(six.text_type)


class SubjectRulesReviewStatus(Model):
    """
    SubjectRulesReviewStatus contains the result of a rules check. This check can
    be incomplete depending on the set of authorizers the server is configured with
    and any errors experienced during evaluation. Because authorization rules are
    additive, if a rule appears in a list it's safe to assume the subject has that
    permission, even if that list is incomplete.
    """

    evaluationError = Field(six.text_type)
    incomplete = RequiredField(bool)
    nonResourceRules = ListField(NonResourceRule)
    resourceRules = ListField(ResourceRule)


class SelfSubjectRulesReview(Model):
    """
    SelfSubjectRulesReview enumerates the set of actions the current user can
    perform within a namespace. The returned list of actions may be incomplete
    depending on the server's authorization mode, and any errors experienced during
    the evaluation. SelfSubjectRulesReview should be used by UIs to show/hide
    actions, or to quickly let an end user reason about their permissions. It
    should NOT Be used by external systems to drive authorization decisions as this
    raises confused deputy, cache lifetime/revocation, and correctness concerns.
    SubjectAccessReview, and LocalAccessReview are the correct way to defer
    authorization decisions to the API server.
    """

    class Meta:
        create_url = "/apis/authorization.k8s.io/v1beta1/selfsubjectrulesreviews"

    apiVersion = Field(six.text_type, "authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "SelfSubjectRulesReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SelfSubjectRulesReviewSpec)
    status = Field(SubjectRulesReviewStatus)


class NonResourceAttributes(Model):
    """
    NonResourceAttributes includes the authorization attributes available for non-
    resource requests to the Authorizer interface
    """

    path = Field(six.text_type)
    verb = Field(six.text_type)


class SubjectAccessReviewSpec(Model):
    """
    SubjectAccessReviewSpec is a description of the access request.  Exactly one of
    ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be
    set
    """

    extra = Field(dict)
    group = ListField(six.text_type)
    nonResourceAttributes = Field(NonResourceAttributes)
    resourceAttributes = Field(ResourceAttributes)
    uid = Field(six.text_type)
    user = Field(six.text_type)


class SubjectAccessReview(Model):
    """
    SubjectAccessReview checks whether or not a user or group can perform an
    action.
    """

    class Meta:
        create_url = "/apis/authorization.k8s.io/v1beta1/subjectaccessreviews"

    apiVersion = Field(six.text_type, "authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "SubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)


class LocalSubjectAccessReview(Model):
    """
    LocalSubjectAccessReview checks whether or not a user or group can perform an
    action in a given namespace. Having a namespace scoped resource makes it much
    easier to grant namespace scoped policy that includes permissions checking.
    """

    class Meta:
        create_url = "/apis/authorization.k8s.io/v1beta1/namespaces/{namespace}/localsubjectaccessreviews"

    apiVersion = Field(six.text_type, "authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "LocalSubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)


class SelfSubjectAccessReviewSpec(Model):
    """
    SelfSubjectAccessReviewSpec is a description of the access request.  Exactly
    one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes
    must be set
    """

    nonResourceAttributes = Field(NonResourceAttributes)
    resourceAttributes = Field(ResourceAttributes)


class SelfSubjectAccessReview(Model):
    """
    SelfSubjectAccessReview checks whether or the current user can perform an
    action.  Not filling in a spec.namespace means 'in all namespaces'.  Self is a
    special case, because users should always be able to check whether they can
    perform an action
    """

    class Meta:
        create_url = "/apis/authorization.k8s.io/v1beta1/selfsubjectaccessreviews"

    apiVersion = Field(six.text_type, "authorization.k8s.io/v1beta1")
    kind = Field(six.text_type, "SelfSubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SelfSubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)
