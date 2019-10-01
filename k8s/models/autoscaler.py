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

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, RequiredField


class CrossVersionObjectReference(Model):
    kind = RequiredField(six.text_type)
    name = RequiredField(six.text_type)
    apiVersion = Field(six.text_type)


class HorizontalPodAutoscalerSpec(Model):
    scaleTargetRef = RequiredField(CrossVersionObjectReference)
    minReplicas = Field(int, 2)
    maxReplicas = RequiredField(int)
    targetCPUUtilizationPercentage = Field(int, 50)


class HorizontalPodAutoscaler(Model):
    class Meta:
        url_template = "/apis/autoscaling/v1/namespaces/{namespace}/horizontalpodautoscalers/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(HorizontalPodAutoscalerSpec)
