#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

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


class CertificateSigningRequestSpec(Model):
    """
    This information is immutable after the request is created. Only the Request
    and Usages fields can be set on creation, other fields are derived by
    Kubernetes and cannot be modified by users.
    """

    extra = Field(dict)
    groups = ListField(six.text_type)
    request = RequiredField(six.text_type)
    uid = Field(six.text_type)
    usages = ListField(six.text_type)
    username = Field(six.text_type)


class CertificateSigningRequestCondition(Model):
    """
    
    """

    lastUpdateTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    type = RequiredField(six.text_type)


class CertificateSigningRequestStatus(Model):
    """
    
    """

    certificate = Field(six.text_type)
    conditions = ListField(CertificateSigningRequestCondition)


class CertificateSigningRequest(Model):
    """
    Describes a certificate signing request
    """
    class Meta:
        create_url = "/apis/certificates.k8s.io/v1beta1/certificatesigningrequests"
        delete_url = "/apis/certificates.k8s.io/v1beta1/certificatesigningrequests/{name}"
        get_url = "/apis/certificates.k8s.io/v1beta1/certificatesigningrequests/{name}"
        list_all_url = "/apis/certificates.k8s.io/v1beta1/certificatesigningrequests"
        update_url = "/apis/certificates.k8s.io/v1beta1/certificatesigningrequests/{name}"
        watch_url = "/apis/certificates.k8s.io/v1beta1/watch/certificatesigningrequests/{name}"
        watchlist_all_url = "/apis/certificates.k8s.io/v1beta1/watch/certificatesigningrequests"
    
    apiVersion = Field(six.text_type, "certificates.k8s.io/v1beta1")
    kind = Field(six.text_type, "CertificateSigningRequest")

    metadata = Field(ObjectMeta)
    spec = Field(CertificateSigningRequestSpec)
    status = Field(CertificateSigningRequestStatus)


class CertificateSigningRequestList(Model):
    """
    
    """
    apiVersion = Field(six.text_type, "certificates.k8s.io/v1beta1")
    kind = Field(six.text_type, "CertificateSigningRequestList")

    items = ListField(CertificateSigningRequest)
    metadata = Field(ListMeta)

