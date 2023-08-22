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


class PolicyRule(Model):
    apiGroups = ListField(str)
    resources = ListField(str)
    verbs = ListField(str)
    resourceNames = ListField(str)
    nonResourceURLs = ListField(str)


class Role(Model):
    class Meta:
        list_url = "/apis/rbac.authorization.k8s.io/v1/roles"
        url_template = "/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/roles/{name}"

    metadata = Field(ObjectMeta)
    rules = ListField(PolicyRule)
