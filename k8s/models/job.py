#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

from .pod import PodTemplateSpec
from .common import ObjectMeta
from ..base import Model
from ..fields import Field


class JobSpec(Model):
    template = Field(PodTemplateSpec)
    backoffLimit = Field(int)


class Job(Model):
    class Meta:
        url_template = "/apis/batch/v1/namespaces/{namespace}/jobs"

    metadata = Field(ObjectMeta)
    spec = Field(JobSpec)
