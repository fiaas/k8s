#!/usr/bin/env python
# -*- coding: utf-8

# Copyright 2017-2020 The FIAAS Authors
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

import datetime

from .common import ObjectMeta, ObjectReference
from .job import JobTemplateSpec
from ..base import Model
from ..fields import Field, ListField, ReadOnlyField


class CronJobSpec(Model):
    concurrencyPolicy = Field(six.text_type)
    failedJobsHistoryLimit = Field(int)
    jobTemplate = Field(JobTemplateSpec)
    schedule = Field(six.text_type)
    startingDeadlineSeconds = Field(int)
    successfulJobsHistoryLimit = Field(int)
    suspend = Field(bool)


class CronJobStatus(Model):
    active = ListField(ObjectReference)
    lastScheduleTime = ReadOnlyField(datetime.datetime)


class CronJob(Model):
    class Meta:
        list_url = "/apis/batch/v1beta1/cronjobs"
        url_template = "/apis/batch/v1beta1/namespaces/{namespace}/cronjobs/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(CronJobSpec)
    status = Field(CronJobStatus)


