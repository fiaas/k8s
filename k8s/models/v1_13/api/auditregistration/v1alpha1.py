#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_13.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class WebhookThrottleConfig(Model):
    """
    WebhookThrottleConfig holds the configuration for throttling events
    """

    burst = Field(int)
    qps = Field(int)


class ServiceReference(Model):
    """
    ServiceReference holds a reference to Service.legacy.k8s.io
    """

    name = RequiredField(six.text_type)
    namespace = RequiredField(six.text_type)
    path = Field(six.text_type)


class WebhookClientConfig(Model):
    """
    WebhookClientConfig contains the information to make a connection with the
    webhook
    """

    caBundle = Field(six.text_type)
    service = Field(ServiceReference)
    url = Field(six.text_type)


class Webhook(Model):
    """
    Webhook holds the configuration of the webhook
    """

    clientConfig = RequiredField(WebhookClientConfig)
    throttle = Field(WebhookThrottleConfig)


class Policy(Model):
    """
    Policy defines the configuration of how audit events are logged
    """

    level = RequiredField(six.text_type)
    stages = ListField(six.text_type)


class AuditSinkSpec(Model):
    """
    AuditSinkSpec holds the spec for the audit sink
    """

    policy = RequiredField(Policy)
    webhook = RequiredField(Webhook)


class AuditSink(Model):
    """
    AuditSink represents a cluster level audit sink
    """
    class Meta:
        create_url = "/apis/auditregistration.k8s.io/v1alpha1/auditsinks"
        delete_url = "/apis/auditregistration.k8s.io/v1alpha1/auditsinks/{name}"
        get_url = "/apis/auditregistration.k8s.io/v1alpha1/auditsinks/{name}"
        list_all_url = "/apis/auditregistration.k8s.io/v1alpha1/auditsinks"
        update_url = "/apis/auditregistration.k8s.io/v1alpha1/auditsinks/{name}"
        watch_url = "/apis/auditregistration.k8s.io/v1alpha1/watch/auditsinks/{name}"
        watchlist_all_url = "/apis/auditregistration.k8s.io/v1alpha1/watch/auditsinks"
    
    apiVersion = Field(six.text_type, "auditregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "AuditSink")

    metadata = Field(ObjectMeta)
    spec = Field(AuditSinkSpec)


class AuditSinkList(Model):
    """
    AuditSinkList is a list of AuditSink items.
    """
    apiVersion = Field(six.text_type, "auditregistration.k8s.io/v1alpha1")
    kind = Field(six.text_type, "AuditSinkList")

    items = ListField(AuditSink)
    metadata = Field(ListMeta)

