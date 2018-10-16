#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, OnceField, ListField


class NodeSpec(Model):
    externalID = OnceField(six.text_type)


class NodeStatus(Model):
    addresses = ListField(dict)
    conditions = ListField(dict)
    nodeInfo = Field(dict)


class Node(Model):
    class Meta:
        list_url = "/api/v1/nodes"
        url_template = "/api/v1/nodes/{name}"
        watch_list_url = "/api/v1/watch/nodes"

    metadata = Field(ObjectMeta)
    spec = Field(NodeSpec)
    status = Field(NodeStatus)
