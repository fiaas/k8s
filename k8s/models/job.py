#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

from .pod import PodTemplateSpec
from .common import ObjectMeta
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


class Job(Model):
    class Meta:
        list_url = "/apis/batch/v1/jobs"
        url_template = "/apis/batch/v1/namespaces/{namespace}/jobs"

    metadata = Field(ObjectMeta)
    spec = Field(JobSpec)
