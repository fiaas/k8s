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

from .common import ObjectMeta
from .pod import PodTemplateSpec
from ..base import Model
from ..fields import Field


class LabelSelector(Model):
    matchLabels = Field(dict)


class JobSpec(Model):
    template = Field(PodTemplateSpec)
    backoffLimit = Field(int)
    activeDeadlineSeconds = Field(int)
    completions = Field(int)
    manualSelector = Field(bool)
    parallelism = Field(int)
    selector = Field(LabelSelector)


class JobTemplateSpec(Model):
    metadata = Field(ObjectMeta)
    spec = Field(JobSpec)


class Job(Model):
    class Meta:
        list_url = "/apis/batch/v1/jobs"
        url_template = "/apis/batch/v1/namespaces/{namespace}/jobs"

    metadata = Field(ObjectMeta)
    spec = Field(JobSpec)
