#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import pytest

from k8s import config
from k8s.base import Model, Field
from k8s.client import Client, SENSITIVE_HEADERS


@pytest.mark.usefixtures("k8s_config")
class TestClient(object):
    @pytest.fixture
    def success_response(self):
        resp = mock.MagicMock()
        resp.status_code = 200
        return resp

    @pytest.fixture
    def session(self, success_response):
        with mock.patch("k8s.client.Client._session") as mockk:
            mockk.request.return_value = success_response
            yield mockk

    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def url(self):
        return "/api/v1/nodes"

    @pytest.fixture
    def explicit_timeout(self):
        return 60

    def test_get_should_use_default_timeout(self, session, client, url):
        client.get(url)
        session.request.assert_called_once_with("GET", _absolute_url(url), json=None, timeout=config.timeout)

    def test_get_should_propagate_timeout(self, session, client, url, explicit_timeout):
        client.get(url, timeout=explicit_timeout)
        session.request.assert_called_once_with("GET", _absolute_url(url), json=None, timeout=explicit_timeout)

    def test_delete_should_use_default_timeout(self, session, client, url):
        client.delete(url)
        session.request.assert_called_once_with(
            "DELETE", _absolute_url(url), json=None, timeout=config.timeout
        )

    def test_delete_should_propagate_timeout(self, session, client, url, explicit_timeout):
        client.delete(url, timeout=explicit_timeout)
        session.request.assert_called_once_with("DELETE", _absolute_url(url), json=None, timeout=explicit_timeout)

    def test_delete_should_use_default_body(self, session, client, url):
        client.delete(url)
        session.request.assert_called_once_with(
            "DELETE", _absolute_url(url), json=None, timeout=config.timeout
        )

    def test_delete_should_propagate_body(self, session, client, url):
        body = {"kind": "DeleteOptions", "apiVersion": "v1", "propagationPolicy": "Foreground"}
        client.delete(url, body=body)
        session.request.assert_called_once_with(
            "DELETE", _absolute_url(url), json=body, timeout=config.timeout
        )

    def test_post_should_use_default_timeout(self, session, client, url):
        body = {"foo": "bar"}
        client.post(url, body=body)
        session.request.assert_called_once_with("POST", _absolute_url(url), json=body, timeout=config.timeout)

    def test_post_should_propagate_timeout(self, session, client, url, explicit_timeout):
        body = {"foo": "bar"}
        client.post(url, body=body, timeout=explicit_timeout)
        session.request.assert_called_once_with("POST", _absolute_url(url), json=body, timeout=explicit_timeout)

    def test_put_should_use_default_timeout(self, session, client, url):
        body = {"foo": "bar"}
        client.put(url, body=body)
        session.request.assert_called_once_with("PUT", _absolute_url(url), json=body, timeout=config.timeout)

    def test_put_should_propagate_timeout(self, session, client, url, explicit_timeout):
        body = {"foo": "bar"}
        client.put(url, body=body, timeout=explicit_timeout)
        session.request.assert_called_once_with("PUT", _absolute_url(url), json=body, timeout=explicit_timeout)

    def test_watch_list_should_raise_exception_when_watch_list_url_is_not_set_on_metaclass(self, session):
        with pytest.raises(NotImplementedError):
            list(WatchListExampleUnsupported.watch_list())

    def test_watch_list_with_namespace_should_raise_exception_when_watch_list_url_template_is_not_set_on_metaclass(self, session):
        with pytest.raises(NotImplementedError):
            list(WatchListExampleUnsupported.watch_list(namespace="explicitly-set"))

    def test_watch_list(self, session):
        list(WatchListExample.watch_list())
        session.request.assert_called_once_with(
            "GET", _absolute_url("/watch/example"), json=None, timeout=None, stream=True
        )

    def test_watch_list_with_namespace(self, session):
        list(WatchListExample.watch_list(namespace="explicitly-set"))
        session.request.assert_called_once_with(
            "GET", _absolute_url("/watch/explicitly-set/example"), json=None, timeout=None, stream=True
        )

    def test_list_without_namespace_should_raise_exception_when_list_url_is_not_set_on_metaclass(self, session):
        with pytest.raises(NotImplementedError):
            WatchListExampleUnsupported.list(namespace=None)

    def test_list_default_namespace(self, session):
        WatchListExample.list()
        session.request.assert_called_once_with(
            "GET", _absolute_url("/apis/namespaces/default/example"), json=None, timeout=config.timeout
        )

    def test_list_explicit_namespace(self, session):
        WatchListExample.list(namespace="explicitly-set")
        session.request.assert_called_once_with(
            "GET", _absolute_url("/apis/namespaces/explicitly-set/example"), json=None, timeout=config.timeout
        )

    def test_list_without_namespace(self, session):
        WatchListExample.list(namespace=None)
        session.request.assert_called_once_with(
            "GET", _absolute_url("/example/list"), json=None, timeout=config.timeout
        )

    def test_find_without_namespace_should_raise_exception_when_list_url_is_not_set_on_metaclass(self, session):
        with pytest.raises(NotImplementedError):
            list(WatchListExampleUnsupported.find("foo", namespace=None))

    def test_find_default_namespace(self, session):
        WatchListExample.find("foo")
        session.request.assert_called_once_with(
            "GET", _absolute_url("/apis/namespaces/default/example"), json=None, timeout=config.timeout,
            params={"labelSelector": "app=foo"}
        )

    def test_find_explicit_namespace(self, session):
        WatchListExample.find("foo", namespace="explicitly-set")
        session.request.assert_called_once_with(
            "GET", _absolute_url("/apis/namespaces/explicitly-set/example"), json=None, timeout=config.timeout,
            params={"labelSelector": "app=foo"}
        )

    def test_find_without_namespace(self, session):
        WatchListExample.find("foo", namespace=None)
        session.request.assert_called_once_with(
            "GET", _absolute_url("/example/list"), json=None, timeout=config.timeout,
            params={"labelSelector": "app=foo"}
        )

    @pytest.mark.parametrize("key", SENSITIVE_HEADERS)
    def test_redacts_sensitive_headers(self, key):
        message = []
        sensitive_value = "super sensitive data that should not be exposed"
        Client._add_headers(message, {key: sensitive_value}, "")
        text = "".join(message)
        assert sensitive_value not in text


def _absolute_url(url):
    return config.api_server + url


class WatchListExample(Model):
    class Meta:
        list_url = "/example/list"
        url_template = "/apis/namespaces/{namespace}/example"
        watch_list_url = "/watch/example"
        watch_list_url_template = "/watch/{namespace}/example"

    value = Field(int)


class WatchListExampleUnsupported(Model):
    class Meta:
        url_template = "/example"

    value = Field(int)
