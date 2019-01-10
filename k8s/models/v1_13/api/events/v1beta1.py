#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_13.api.core.v1 import EventSource, ObjectReference
from k8s.models.v1_13.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class EventSeries(Model):
    """
    EventSeries contain information on series of events, i.e. thing that was/is
    happening continuously for some time.
    """

    count = RequiredField(int)
    lastObservedTime = RequiredField(datetime.datetime)
    state = RequiredField(six.text_type)


class Event(Model):
    """
    Event is a report of an event somewhere in the cluster. It generally denotes
    some state change in the system.
    """
    class Meta:
        create_url = "/apis/events.k8s.io/v1beta1/namespaces/{namespace}/events"
        delete_url = "/apis/events.k8s.io/v1beta1/namespaces/{namespace}/events/{name}"
        get_url = "/apis/events.k8s.io/v1beta1/namespaces/{namespace}/events/{name}"
        list_all_url = "/apis/events.k8s.io/v1beta1/events"
        list_ns_url = "/apis/events.k8s.io/v1beta1/namespaces/{namespace}/events"
        update_url = "/apis/events.k8s.io/v1beta1/namespaces/{namespace}/events/{name}"
        watch_url = "/apis/events.k8s.io/v1beta1/watch/namespaces/{namespace}/events/{name}"
        watchlist_all_url = "/apis/events.k8s.io/v1beta1/watch/events"
        watchlist_ns_url = "/apis/events.k8s.io/v1beta1/watch/namespaces/{namespace}/events"
    
    apiVersion = Field(six.text_type, "events.k8s.io/v1beta1")
    kind = Field(six.text_type, "Event")

    action = Field(six.text_type)
    deprecatedCount = Field(int)
    deprecatedFirstTimestamp = Field(datetime.datetime)
    deprecatedLastTimestamp = Field(datetime.datetime)
    deprecatedSource = Field(EventSource)
    eventTime = RequiredField(datetime.datetime)
    metadata = Field(ObjectMeta)
    note = Field(six.text_type)
    reason = Field(six.text_type)
    regarding = Field(ObjectReference)
    related = Field(ObjectReference)
    reportingController = Field(six.text_type)
    reportingInstance = Field(six.text_type)
    series = Field(EventSeries)
    type = Field(six.text_type)


class EventList(Model):
    """
    EventList is a list of Event objects.
    """
    apiVersion = Field(six.text_type, "events.k8s.io/v1beta1")
    kind = Field(six.text_type, "EventList")

    items = ListField(Event)
    metadata = Field(ListMeta)

