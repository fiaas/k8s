#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from k8s.base import Model
from k8s.fields import RequiredField


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class Info(Model):
    """
    Info contains versioning information. how we'll want to distribute that
    information.
    """

    buildDate = RequiredField(six.text_type)
    compiler = RequiredField(six.text_type)
    gitCommit = RequiredField(six.text_type)
    gitTreeState = RequiredField(six.text_type)
    gitVersion = RequiredField(six.text_type)
    goVersion = RequiredField(six.text_type)
    major = RequiredField(six.text_type)
    minor = RequiredField(six.text_type)
    platform = RequiredField(six.text_type)

