#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField
from k8s.models.v1_7.apimachinery.apis.meta.v1 import LabelSelector, ListMeta, ObjectMeta
from k8s.models.v1_7.kubernetes.api.v1 import PodTemplateSpec


class JobCondition(Model):
    """
    JobCondition describes current state of a job.
    """

    lastProbeTime = Field(datetime.datetime)
    lastTransitionTime = Field(datetime.datetime)
    message = Field(six.text_type)
    reason = Field(six.text_type)
    status = Field(six.text_type)
    type = Field(six.text_type)


class JobStatus(Model):
    """
    JobStatus represents the current state of a Job.
    """

    active = Field(int)
    completionTime = Field(datetime.datetime)
    conditions = ListField(JobCondition)
    failed = Field(int)
    startTime = Field(datetime.datetime)
    succeeded = Field(int)


class JobSpec(Model):
    """
    JobSpec describes how the job execution will look like.
    """

    activeDeadlineSeconds = Field(int)
    completions = Field(int)
    manualSelector = Field(bool)
    parallelism = Field(int)
    selector = Field(LabelSelector)
    template = Field(PodTemplateSpec)


class Job(Model):
    """
    Job represents the configuration of a single job.
    """
    class Meta:
        create_url = "/apis/batch/v1/namespaces/{namespace}/jobs"
        delete_url = "/apis/batch/v1/namespaces/{namespace}/jobs/{name}"
        get_url = "/apis/batch/v1/namespaces/{namespace}/jobs/{name}"
        list_all_url = "/apis/batch/v1/jobs"
        list_ns_url = "/apis/batch/v1/namespaces/{namespace}/jobs"
        update_url = "/apis/batch/v1/namespaces/{namespace}/jobs/{name}"
        watch_url = "/apis/batch/v1/watch/namespaces/{namespace}/jobs/{name}"
        watchlist_all_url = "/apis/batch/v1/watch/jobs"
        watchlist_ns_url = "/apis/batch/v1/watch/namespaces/{namespace}/jobs"
    
    apiVersion = Field(six.text_type, "batch/v1")
    kind = Field(six.text_type, "Job")

    metadata = Field(ObjectMeta)
    spec = Field(JobSpec)
    status = Field(JobStatus)


class JobList(Model):
    """
    JobList is a collection of jobs.
    """
    apiVersion = Field(six.text_type, "batch/v1")
    kind = Field(six.text_type, "JobList")

    items = ListField(Job)
    metadata = Field(ListMeta)

