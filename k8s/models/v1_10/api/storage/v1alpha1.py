#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import datetime

import six

from k8s.base import Model
from k8s.fields import Field, ListField, RequiredField
from k8s.models.v1_10.apimachinery.apis.meta.v1 import ListMeta, ObjectMeta


###############################################################################
# This file is auto-generated! Do not edit!
#
# Codestyle checking is disabled for this file
# flake8: noqa
###############################################################################


class VolumeError(Model):
    """
    VolumeError captures an error encountered during a volume operation.
    """

    message = Field(six.text_type)
    time = Field(datetime.datetime)


class VolumeAttachmentStatus(Model):
    """
    VolumeAttachmentStatus is the status of a VolumeAttachment request.
    """

    attachError = Field(VolumeError)
    attached = RequiredField(bool)
    attachmentMetadata = Field(dict)
    detachError = Field(VolumeError)


class VolumeAttachmentSource(Model):
    """
    VolumeAttachmentSource represents a volume that should be attached. Right now
    only PersistenVolumes can be attached via external attacher, in future we may
    allow also inline volumes in pods. Exactly one member can be set.
    """

    persistentVolumeName = Field(six.text_type)


class VolumeAttachmentSpec(Model):
    """
    VolumeAttachmentSpec is the specification of a VolumeAttachment request.
    """

    attacher = RequiredField(six.text_type)
    nodeName = RequiredField(six.text_type)
    source = RequiredField(VolumeAttachmentSource)


class VolumeAttachment(Model):
    """
    VolumeAttachment captures the intent to attach or detach the specified volume
    to/from the specified node.

    VolumeAttachment objects are non-namespaced.
    """
    class Meta:
        create_url = "/apis/storage.k8s.io/v1alpha1/volumeattachments"
        delete_url = "/apis/storage.k8s.io/v1alpha1/volumeattachments/{name}"
        get_url = "/apis/storage.k8s.io/v1alpha1/volumeattachments/{name}"
        list_all_url = "/apis/storage.k8s.io/v1alpha1/volumeattachments"
        update_url = "/apis/storage.k8s.io/v1alpha1/volumeattachments/{name}"
        watch_url = "/apis/storage.k8s.io/v1alpha1/watch/volumeattachments/{name}"
        watchlist_all_url = "/apis/storage.k8s.io/v1alpha1/watch/volumeattachments"
    
    apiVersion = Field(six.text_type, "storage.k8s.io/v1alpha1")
    kind = Field(six.text_type, "VolumeAttachment")

    metadata = Field(ObjectMeta)
    spec = RequiredField(VolumeAttachmentSpec)
    status = Field(VolumeAttachmentStatus)


class VolumeAttachmentList(Model):
    """
    VolumeAttachmentList is a collection of VolumeAttachment objects.
    """
    apiVersion = Field(six.text_type, "storage.k8s.io/v1alpha1")
    kind = Field(six.text_type, "VolumeAttachmentList")

    items = ListField(VolumeAttachment)
    metadata = Field(ListMeta)

