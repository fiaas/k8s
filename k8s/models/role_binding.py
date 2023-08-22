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


from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField


class RoleRef(Model):
    apiGroup = Field(str)
    kind = Field(str)
    name = Field(str)


class Subject(Model):
    kind = Field(str)
    name = Field(str)
    apiGroup = Field(str)
    namespace = Field(str)


class RoleBinding(Model):
    class Meta:
        list_url = "/apis/rbac.authorization.k8s.io/v1/rolebindings"
        url_template = "/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}"

    metadata = Field(ObjectMeta)
    roleRef = Field(RoleRef)
    subjects = ListField(Subject)
