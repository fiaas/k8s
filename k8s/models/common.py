#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

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
    name = Field(six.text_type)
    namespace = Field(six.text_type, "default")
    resourceVersion = ReadOnlyField(six.text_type)
    labels = Field(dict)
    annotations = Field(dict)
    generateName = Field(six.text_type)
    ownerReferences = ListField(OwnerReference)
    selfLink = ReadOnlyField(six.text_type)
    uid = ReadOnlyField(six.text_type)
    generation = ReadOnlyField(int)
