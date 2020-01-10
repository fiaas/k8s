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
from .pod import PodTemplateSpec
from ..base import Model
from ..fields import Field


class LabelSelector(Model):
    matchLabels = Field(dict)


class RollingUpdateDeployment(Model):
    maxUnavailable = Field(int, alt_type=six.text_type)
    maxSurge = Field(int, alt_type=six.text_type)


class DeploymentStrategy(Model):
    type = Field(six.text_type, "RollingUpdate")
    rollingUpdate = Field(RollingUpdateDeployment)


class DeploymentSpec(Model):
    replicas = Field(int, 1)
    selector = Field(LabelSelector)
    template = Field(PodTemplateSpec)
    strategy = Field(DeploymentStrategy)
    minReadySeconds = Field(six.text_type, alt_type=int)
    revisionHistoryLimit = Field(int)
    paused = Field(six.text_type)


class DeploymentStatus(Model):
    observedGeneration = Field(int)
    replicas = Field(int)
    updatedReplicas = Field(int)
    availableReplicas = Field(int)
    unavailableReplicas = Field(int)


class Deployment(Model):
    class Meta:
        list_url = "/apis/apps/v1/deployments"
        url_template = "/apis/apps/v1/namespaces/{namespace}/deployments/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(DeploymentSpec)
    status = Field(DeploymentStatus)
