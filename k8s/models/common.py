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

import datetime

from ..base import Model
from ..fields import Field, ReadOnlyField, ListField


class OwnerReference(Model):
    apiVersion = Field(str)
    blockOwnerDeletion = Field(bool)
    controller = Field(bool)
    kind = Field(str)
    name = Field(str)
    uid = Field(str)


class ObjectMeta(Model):
    annotations = Field(dict)
    creationTimestamp = ReadOnlyField(datetime.datetime)
    deletionGracePeriodSeconds = ReadOnlyField(int)
    deletionTimestamp = ReadOnlyField(datetime.datetime)
    finalizers = ListField(str)
    generateName = Field(str)
    generation = ReadOnlyField(int)
    labels = Field(dict)
    name = Field(str)
    namespace = Field(str, "default")
    ownerReferences = ListField(OwnerReference)
    resourceVersion = ReadOnlyField(str)
    selfLink = ReadOnlyField(str)
    uid = ReadOnlyField(str)


class TypedLocalObjectReference(Model):
    apiGroup = Field(str)
    kind = Field(str)
    name = Field(str)


class ObjectReference(Model):
    apiVersion = Field(str)
    fieldPath = Field(str)
    kind = Field(str)
    name = Field(str)
    namespace = Field(str)
    resourceVersion = Field(str)
    uid = Field(str)


class Preconditions(Model):
    resourceVersion = Field(str)
    uid = Field(str)


class DeleteOptions(Model):
    apiVersion = Field(str)
    dryRun = ListField(str)
    gracePeriodSeconds = Field(int)
    kind = Field(str)
    preconditions = Field(Preconditions)
    propagationPolicy = Field(str)


class LocalObjectReference(Model):
    name = Field(str)
