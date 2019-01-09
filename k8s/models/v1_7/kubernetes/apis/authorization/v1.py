#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class NonResourceAttributes(Model):
    """
    NonResourceAttributes includes the authorization attributes available for non-
    resource requests to the Authorizer interface
    """

    path = Field(six.text_type)
    verb = Field(six.text_type)


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


class SubjectAccessReviewSpec(Model):
    """
    SubjectAccessReviewSpec is a description of the access request.  Exactly one of
    ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be
    set
    """

    extra = Field(dict)
    groups = ListField(six.text_type)
    nonResourceAttributes = Field(NonResourceAttributes)
    resourceAttributes = Field(ResourceAttributes)
    user = Field(six.text_type)


class SelfSubjectAccessReviewSpec(Model):
    """
    SelfSubjectAccessReviewSpec is a description of the access request.  Exactly
    one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes
    must be set
    """

    nonResourceAttributes = Field(NonResourceAttributes)
    resourceAttributes = Field(ResourceAttributes)


class SubjectAccessReviewStatus(Model):
    """
    SubjectAccessReviewStatus
    """

    allowed = RequiredField(bool)
    evaluationError = Field(six.text_type)
    reason = Field(six.text_type)


class SubjectAccessReview(Model):
    """
    SubjectAccessReview checks whether or not a user or group can perform an
    action.
    """
    class Meta:
        create_url = "/apis/authorization.k8s.io/v1/subjectaccessreviews"
    
    apiVersion = Field(six.text_type, "authorization.k8s.io/v1")
    kind = Field(six.text_type, "SubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)


class SelfSubjectAccessReview(Model):
    """
    SelfSubjectAccessReview checks whether or the current user can perform an
    action.  Not filling in a spec.namespace means 'in all namespaces'.  Self is a
    special case, because users should always be able to check whether they can
    perform an action
    """
    class Meta:
        create_url = "/apis/authorization.k8s.io/v1/selfsubjectaccessreviews"
    
    apiVersion = Field(six.text_type, "authorization.k8s.io/v1")
    kind = Field(six.text_type, "SelfSubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SelfSubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)


class LocalSubjectAccessReview(Model):
    """
    LocalSubjectAccessReview checks whether or not a user or group can perform an
    action in a given namespace. Having a namespace scoped resource makes it much
    easier to grant namespace scoped policy that includes permissions checking.
    """
    class Meta:
        create_url = "/apis/authorization.k8s.io/v1/namespaces/{namespace}/localsubjectaccessreviews"
    
    apiVersion = Field(six.text_type, "authorization.k8s.io/v1")
    kind = Field(six.text_type, "LocalSubjectAccessReview")

    metadata = Field(ObjectMeta)
    spec = RequiredField(SubjectAccessReviewSpec)
    status = Field(SubjectAccessReviewStatus)

