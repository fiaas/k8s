#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class LabelSelectorRequirement(Model):
    key = Field(six.text_type)
    operator = Field(six.text_type)
    values = ListField(six.text_type)


class LabelSelector(Model):
    matchExpressions = Field(LabelSelectorRequirement)
    matchLabels = Field(dict)


class PodDisruptionBudgetSpec(Model):
    minAvailable = Field(six.text_type, alt_type=int)
    maxUnavailable = Field(six.text_type, alt_type=int)
    selector = Field(LabelSelector)


class PodDisruptionBudget(Model):
    class Meta:
        list_url = "/apis/policy/v1beta1/poddisruptionbudgets"
        url_template = "/apis/policy/v1beta1/namespaces/{namespace}/poddisruptionbudgets/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(PodDisruptionBudgetSpec)
