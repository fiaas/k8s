#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2019 The FIAAS Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


class TypedLocalObjectReference(Model):
    apiGroup = Field(six.text_type)
    kind = Field(six.text_type)
    name = Field(six.text_type)


class ObjectReference(Model):
    apiVersion = Field(six.text_type)
    fieldPath = Field(six.text_type)
    kind = Field(six.text_type)
    name = Field(six.text_type)
    namespace = Field(six.text_type)
    resourceVersion = Field(six.text_type)
    uid = Field(six.text_type)


class Preconditions(Model):
    resourceVersion = Field(six.text_type)
    uid = Field(six.text_type)


class DeleteOptions(Model):
    apiVersion = Field(six.text_type)
    dryRun = ListField(six.text_type)
    gracePeriodSeconds = Field(int)
    kind = Field(six.text_type)
    preconditions = Field(Preconditions)
    propagationPolicy = Field(six.text_type)


class LocalObjectReference(Model):
    name = Field(six.text_type)
