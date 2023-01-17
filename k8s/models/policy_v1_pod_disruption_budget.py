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

import six

from .common import ObjectMeta, LabelSelector
from ..base import Model
from ..fields import Field


class PodDisruptionBudgetSpec(Model):
    minAvailable = Field(six.text_type, alt_type=int)
    maxUnavailable = Field(six.text_type, alt_type=int)
    selector = Field(LabelSelector)


class PodDisruptionBudgetStatus(Model):
    observedGeneration = Field(int)
    disruptedPods = Field(dict)
    disruptionsAllowed = Field(int)
    currentHealthy = Field(int)
    desiredHealthy = Field(int)
    expectedPods = Field(int)


class PodDisruptionBudget(Model):
    class Meta:
        list_url = "/apis/policy/v1/poddisruptionbudgets"
        url_template = "/apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(PodDisruptionBudgetSpec)
    status = Field(PodDisruptionBudgetStatus)
