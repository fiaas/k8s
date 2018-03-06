from __future__ import absolute_import

from .common import ObjectMeta
from ..base import Model
from ..fields import Field


class ConfigMap(Model):
    class Meta:
        list_url = "/api/v1/configmaps"
        url_template = "/api/v1/namespaces/{namespace}/configmaps/{name}"

    metadata = Field(ObjectMeta)
    data = Field(dict)
