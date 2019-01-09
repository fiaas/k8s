#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import Field


class Info(Model):
    """
    Info contains versioning information. how we'll want to distribute that
    information.
    """

    buildDate = Field(six.text_type)
    compiler = Field(six.text_type)
    gitCommit = Field(six.text_type)
    gitTreeState = Field(six.text_type)
    gitVersion = Field(six.text_type)
    goVersion = Field(six.text_type)
    major = Field(six.text_type)
    minor = Field(six.text_type)
    platform = Field(six.text_type)

