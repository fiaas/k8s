#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from ..base import Model
from ..fields import Field, ReadOnlyField, ListField


class OwnerReference(Model):
    apiVersion = Field(six.text_type)
    blockOwnerDeletion = Field(bool)
    controller = Field(bool)
    kind = Field(six.text_type)
    name = Field(six.text_type)
    uid = Field(six.text_type)


class ObjectMeta(Model):
    annotations = Field(dict)
    creationTimestamp = ReadOnlyField(datetime.datetime)
    deletionGracePeriodSeconds = ReadOnlyField(int)
    deletionTimestamp = ReadOnlyField(datetime.datetime)
    finalizers = ListField(six.text_type)
    generateName = Field(six.text_type)
    generation = ReadOnlyField(int)
    labels = Field(dict)
    name = Field(six.text_type)
    namespace = Field(six.text_type, "default")
    ownerReferences = ListField(OwnerReference)
    resourceVersion = ReadOnlyField(six.text_type)
    selfLink = ReadOnlyField(six.text_type)
    uid = ReadOnlyField(six.text_type)
