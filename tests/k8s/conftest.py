#!/usr/bin/env python
# -*- coding: utf-8

import logging

import pytest
import mock

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
