#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class NamespaceSpec(Model):
    finalizers = ListField(six.text_type)


class Namespace(Model):
    class Meta:
        list_url = "/api/v1/namespaces"
        url_template = "/api/v1/namespaces/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(NamespaceSpec)
