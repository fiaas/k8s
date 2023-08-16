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


from .common import ObjectMeta, LocalObjectReference
from ..base import Model
from ..fields import Field, ListField, RequiredField


class ContainerPort(Model):
    name = Field(str)
    hostPort = Field(int)
    containerPort = Field(int)
    protocol = Field(str, "TCP")


class ObjectFieldSelector(Model):
    apiVersion = Field(str)
    fieldPath = RequiredField(str)


class ResourceFieldSelector(Model):
    containerName = Field(str)
    resource = RequiredField(str)
    divisor = Field(str)


class ConfigMapKeySelector(Model):
    name = Field(str)
    key = RequiredField(str)


class SecretKeySelector(Model):
    name = Field(str)
    key = RequiredField(str)


class EnvVarSource(Model):
    fieldRef = Field(ObjectFieldSelector)
    resourceFieldRef = Field(ResourceFieldSelector)
    configMapKeyRef = Field(ConfigMapKeySelector)
    secretKeyRef = Field(SecretKeySelector)


class SecretEnvSource(Model):
    name = Field(str)
    optional = Field(bool)


class ConfigMapEnvSource(Model):
    name = Field(str)
    optional = Field(bool)


class EnvFromSource(Model):
    configMapRef = Field(ConfigMapEnvSource)
    secretRef = Field(SecretEnvSource)


class EnvVar(Model):
    name = Field(str)
    value = Field(str)
    valueFrom = Field(EnvVarSource)


class ResourceRequirements(Model):
    limits = Field(dict)
    requests = Field(dict)


class VolumeMount(Model):
    name = Field(str)
    readOnly = Field(bool)
    mountPath = Field(str)


class HTTPHeader(Model):
    name = Field(str)
    value = Field(str)


class HTTPGetAction(Model):
    path = Field(str)
    port = Field(str, alt_type=int)
    scheme = Field(str, "HTTP")
    httpHeaders = ListField(HTTPHeader)


class TCPSocketAction(Model):
    port = Field(str, alt_type=int)


class ExecAction(Model):
    command = Field(list)


class Probe(Model):
    httpGet = Field(HTTPGetAction)
    tcpSocket = Field(TCPSocketAction)
    _exec = Field(ExecAction)
    initialDelaySeconds = Field(int, 5)
    timeoutSeconds = Field(int)
    successThreshold = Field(int)
    failureThreshold = Field(int)
    periodSeconds = Field(int)


class Handler(Model):
    httpGet = Field(HTTPGetAction)
    tcpSocket = Field(TCPSocketAction)
    _exec = Field(ExecAction)


class Lifecycle(Model):
    postStart = Field(Handler)
    preStop = Field(Handler)


class Container(Model):
    name = Field(str)
    image = Field(str)
    ports = ListField(ContainerPort)
    env = ListField(EnvVar)
    envFrom = ListField(EnvFromSource)
    resources = Field(ResourceRequirements)
    volumeMounts = ListField(VolumeMount)
    lifecycle = Field(Lifecycle)
    livenessProbe = Field(Probe)
    readinessProbe = Field(Probe)
    imagePullPolicy = Field(str, "IfNotPresent")
    command = ListField(str)
    args = ListField(str)


class SecretVolumeSource(Model):
    secretName = Field(str)
    optional = Field(bool)
    defaultMode = Field(int)


class KeyToPath(Model):
    key = RequiredField(str)
    path = RequiredField(str)


class ConfigMapVolumeSource(Model):
    name = Field(str)
    optional = Field(bool)
    defaultMode = Field(int)


class EmptyDirVolumeSource(Model):
    medium = Field(str)


class NFSVolumeSource(Model):
    path = Field(str)
    readOnly = Field(bool)
    server = Field(str)


class HostPathVolumeSource(Model):
    path = Field(str)


class GCEPersistentDiskVolumeSource(Model):
    fsType = Field(str)
    partition = Field(int)
    pdName = Field(str)
    readOnly = Field(bool)


class AWSElasticBlockStoreVolumeSource(Model):
    fsType = Field(str)
    partition = Field(int)
    readOnly = Field(bool)
    volumeID = Field(str)


class Volume(Model):
    name = Field(str)
    awsElasticBlockStore = Field(AWSElasticBlockStoreVolumeSource)
    configMap = Field(ConfigMapVolumeSource)
    emptyDir = Field(EmptyDirVolumeSource)
    gcePersistentDisk = Field(GCEPersistentDiskVolumeSource)
    hostPath = Field(HostPathVolumeSource)
    nfs = Field(NFSVolumeSource)
    secret = Field(SecretVolumeSource)


class PodSpec(Model):
    volumes = ListField(Volume)
    containers = ListField(Container)
    restartPolicy = Field(str, "Always")
    terminationGracePeriodSeconds = Field(int)
    activeDeadlineSeconds = Field(int)
    dnsPolicy = Field(str, "ClusterFirst")
    nodeName = Field(str)
    nodeSelector = Field(dict)
    selector = Field(dict)
    serviceAccountName = Field(str, "default")
    automountServiceAccountToken = Field(bool)
    imagePullSecrets = ListField(LocalObjectReference)
    initContainers = ListField(Container)


class PodTemplateSpec(Model):
    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)


class Pod(Model):
    class Meta:
        list_url = "/api/v1/pods"
        url_template = "/api/v1/namespaces/{namespace}/pods/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)
