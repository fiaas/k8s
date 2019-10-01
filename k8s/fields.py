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

from __future__ import absolute_import

import copy
from datetime import datetime

import pyrfc3339


class Field(object):
    """Generic field on a k8s model"""

    def __init__(self, type, default_value=None, alt_type=None):
        self.type = type
        self.alt_type = alt_type
        self.name = "__unset__"
        self._default_value = default_value

    def dump(self, instance):
        value = getattr(instance, self.name)
        return self._as_dict(value)

    def load(self, instance, value):
        new_value = self._from_dict(value)
        instance._values[self.name] = new_value

    def set(self, instance, kwargs):
        value = kwargs.get(self.name, self.default_value)
        self.__set__(instance, value)

    def is_valid(self, instance):
        return True

    def is_set(self, instance):
        return instance._values.get(self.name) != self.default_value

    def __get__(self, instance, obj_type=None):
        value = instance._values.get(self.name, self.default_value)
        return value

    def __set__(self, instance, new_value):
        current_value = instance._values.get(self.name)
        if new_value == current_value:
            return
        if new_value is not None:
            try:
                current_value.merge(new_value)
                return
            except AttributeError:
                pass
        instance._values[self.name] = new_value

    def __delete__(self, instance):
        del instance._values[self.name]

    @property
    def default_value(self):
        from .base import Model
        if issubclass(self.type, Model) and self._default_value is None:
            return self.type(new=False)
        return copy.copy(self._default_value)

    def _as_dict(self, value):
        try:
            return value.as_dict()
        except AttributeError:
            """ If we encounter a dict with all None-elements, we return None.
                This is because the Kubernetes-API does not support empty string values, or "null" in json.
            """
            if isinstance(value, dict):
                d = {k: v for k, v in value.items() if v is not None}
                return d if d else None
            elif datetime in (self.type, self.alt_type) and isinstance(value, datetime):
                return pyrfc3339.generate(value, accept_naive=True)
            else:
                return value

    def _from_dict(self, value):
        if value is None:
            return self.default_value
        try:
            return self.type.from_dict(value)
        except AttributeError:
            if isinstance(value, self.type) or (self.alt_type and isinstance(value, self.alt_type)):
                return value
            if self.type is datetime:
                return pyrfc3339.parse(value)
            return self.type(value)

    def __repr__(self):
        return "{}(name={}, type={}, default_value={}, alt_type={})".format(
            self.__class__.__name__,
            self.name,
            self.type,
            self._default_value,
            self.alt_type
        )


class ReadOnlyField(Field):
    """ReadOnlyField can only be set by the API-server"""

    def __set__(self, instance, value):
        pass


class OnceField(Field):
    """OnceField can only be set on new instances, and is immutable after creation on the server"""

    def __set__(self, instance, value):
        if instance._new:
            super(OnceField, self).__set__(instance, value)


class ListField(Field):
    """ListField is a list (array) of a single type on a model"""

    def __init__(self, type, default_value=None):
        if default_value is None:
            default_value = []
        super(ListField, self).__init__(type, default_value)

    def dump(self, instance):
        return [self._as_dict(v) for v in getattr(instance, self.name)]

    def load(self, instance, value):
        if value is None:
            value = self.default_value
        instance._values[self.name] = [self._from_dict(v) for v in value]


class RequiredField(Field):
    """Required field must have a value from the start"""

    def is_valid(self, instance):
        value = self.__get__(instance)
        return value is not None and super(RequiredField, self).is_valid(instance)
