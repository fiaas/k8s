#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_6.apimachinery.apis.meta.v1 import ObjectMeta


class TokenReviewSpec(Model):
    """
    TokenReviewSpec is a description of the token authentication request.
    """

    token = Field(six.text_type)


class UserInfo(Model):
    """
    UserInfo holds the information about the user needed to implement the user.Info
    interface.
    """

    extra = Field(dict)
    groups = ListField(six.text_type)
    uid = Field(six.text_type)
    username = Field(six.text_type)


class TokenReviewStatus(Model):
    """
    TokenReviewStatus is the result of the token authentication request.
    """

    authenticated = Field(bool)
    error = Field(six.text_type)
    user = Field(UserInfo)


class TokenReview(Model):
    """
    TokenReview attempts to authenticate a token to a known user. Note: TokenReview
    requests may be cached by the webhook token authenticator plugin in the kube-
    apiserver.
    """
    class Meta:
        create_url = "/apis/authentication.k8s.io/v1/tokenreviews"
    
    apiVersion = Field(six.text_type, "authentication.k8s.io/v1")
    kind = Field(six.text_type, "TokenReview")

    metadata = Field(ObjectMeta)
    spec = Field(TokenReviewSpec)
    status = Field(TokenReviewStatus)

