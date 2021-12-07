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

    def __init__(self, field_type, default_value=None, alt_type=None, name="__unset__"):
        self.type = field_type
        self.alt_type = alt_type
        self.name = name
        self._default_value = default_value
        self.default_value_create_instance = True

    def dump(self, instance):
        value = getattr(instance, self.attr_name)
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
        if issubclass(self.type, Model) and self.default_value_create_instance and self._default_value is None:
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

    def __init__(self, field_type, default_value=None, name='__unset__'):
        if default_value is None:
            default_value = []
        super(ListField, self).__init__(field_type, default_value, name=name)

    def dump(self, instance):
        return [self._as_dict(v) for v in getattr(instance, self.attr_name)]

    def load(self, instance, value):
        if value is None:
            value = self.default_value
        instance._values[self.name] = [self._from_dict(v) for v in value]


class RequiredField(Field):
    """Required field must have a value from the start"""

    def is_valid(self, instance):
        value = self.__get__(instance)
        return value is not None and super(RequiredField, self).is_valid(instance)


class JSONField(Field):
    """
    Field with allowed types `bool`, `int`, `float`, `str`, `dict`, `list`
    Items of dicts and lists have the same allowed types
    """

    def __init__(self, default_value=None, name="__unset__"):
        self.type = None
        self.alt_type = None
        self.allowed_types = [bool, int, float, str, dict, list]
        self.name = name
        self._default_value = default_value

    def load(self, instance, value):
        if value is None:
            value = self.default_value
        self.__set__(instance, value)

    def is_valid(self, instance):
        value = self.__get__(instance)
        if value is None:
            return True
        try:
            return self._check_allowed_types(value)
        except TypeError:
            return False

    def __set__(self, instance, new_value):
        if (new_value is None) or self._check_allowed_types(new_value, chain=[type(instance).__name__, self.name]):
            instance._values[self.name] = new_value

    def _check_allowed_types(self, value, chain=None):
        if chain is None:
            chain = []
        if any(isinstance(value, t) for t in self.allowed_types):
            if isinstance(value, dict):
                for k, v in value.items():
                    self._check_allowed_types(k, chain.append(k))
                    self._check_allowed_types(v, chain.append(k))
            if isinstance(value, list):
                for v in value:
                    self._check_allowed_types(v, chain.append("[\"{value}\"]".format(value=v)))
            return True
        else:
            def typename(i):
                return i.__name__
            raise TypeError("{name} has invalid type {type}. Allowed types are {allowed_types}.".format(
                name=".".join(chain),
                type=type(value).__name__,
                allowed_types=", ".join(map(typename, self.allowed_types))
            ))

    @property
    def default_value(self):
        return copy.copy(self._default_value)
