#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


Terminating = "Terminating"
NotTerminating = "NotTerminating"
BestEffort = "BestEffort"
NotBestEffort = "NotBestEffort"


class ResourceQuotaSpec(Model):
    hard = Field(dict)
    scopes = ListField(six.text_type)


class ResourceQuotaStatus(Model):
    hard = Field(dict)
    used = Field(dict)


class ResourceQuota(Model):
    class Meta:
        list_url = "/api/v1/resourcequotas"
        url_template = "/api/v1/namespaces/{namespace}/resourcequotas"

    metadata = Field(ObjectMeta)
    spec = Field(ResourceQuotaSpec)
    status = Field(ResourceQuotaStatus)
