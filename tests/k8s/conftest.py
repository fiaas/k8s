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


import logging

import mock
import pytest

from k8s import config


@pytest.yield_fixture
def logger():
    """Set root logger to DEBUG, and add stream handler"""
    root_logger = logging.getLogger()
    old_level = root_logger.getEffectiveLevel()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    root_logger.addHandler(handler)
    yield root_logger
    root_logger.removeHandler(handler)
    root_logger.setLevel(old_level)


@pytest.fixture
def k8s_config(monkeypatch):
    """Configure k8s for test-runs"""
    monkeypatch.setattr(config, "api_server", "http://localhost:8080")
    monkeypatch.setattr(config, "verify_ssl", False)


@pytest.fixture
def post():
    with mock.patch('k8s.client.Client.post') as m:
        yield m


@pytest.fixture
def put():
    with mock.patch('k8s.client.Client.put') as m:
        yield m


@pytest.fixture
def get():
    with mock.patch('k8s.client.Client.get') as m:
        yield m


@pytest.fixture
def delete():
    with mock.patch('k8s.client.Client.delete') as m:
        yield m


@pytest.fixture
def api_get():
    with mock.patch('k8s.base.ApiMixIn.get') as m:
        yield m
