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


from .common import ObjectMeta, LocalObjectReference
from ..base import Model
from ..fields import Field, ListField


class ServiceAccount(Model):
    class Meta:
        list_url = "/api/v1/serviceaccounts"
        url_template = "/api/v1/namespaces/{namespace}/serviceaccounts/{name}"

    metadata = Field(ObjectMeta)
    imagePullSecrets = ListField(LocalObjectReference)
    secrets = ListField(LocalObjectReference)
    automountServiceAccountToken = Field(bool)
