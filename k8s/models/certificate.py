#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2022 The FIAAS Authors
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

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class IssuerReference(Model):
    name = Field(six.text_type)
    kind = Field(six.text_type)
    group = Field(six.text_type)


class CertificateSpec(Model):
    secretName = Field(six.text_type)
    issuerRef = Field(IssuerReference)


class CertificateCondition(Model):
    type = Field(six.text_type)
    status = Field(six.text_type)


class CertificateStatus(Model):
    conditions = ListField(CertificateCondition)
    notAfter = Field(datetime.datetime)


class Certificate(Model):
    class Meta:
        list_url = "/apis/cert-manager.io/v1/certificates"
        url_template = "/apis/cert-manager.io/v1/namespaces/{namespace}/certificates/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(CertificateSpec)
    status = Field(CertificateStatus)
