#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import logging

import requests
from requests import RequestException
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from . import config

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

SENSITIVE_HEADERS = {
    # Wordlist lifted from https://github.com/google/har-sanitizer/blob/master/harsanitizer/static/wordlist.json
    "state",
    "shdf",
    "usg",
    "password",
    "email",
    "code",
    "code_verifier",
    "client_secret",
    "client_id",
    "token",
    "access_token",
    "authenticity_token",
    "id_token",
    "appid",
    "challenge",
    "facetid",
    "assertion",
    "fcparams",
    "serverdata",
    "authorization",
    "auth",
    "x-client-data",
    "samlrequest",
    "samlresponse"
}


class K8sClientException(RequestException):
    pass


class NotFound(K8sClientException):
    """The resource was not found, and the operation could not be completed"""


class ServerError(K8sClientException):
    """The API-server returned an internal error"""


class ClientError(K8sClientException):
    """The client made a bad request"""


def _session_factory():
    """Retry on errors from the API-server. Retry-After header will be respected first, which
    we expect to be set for too_many_requests, and for other errors it will back-off exponentially up
    to the 120s maximum"""
    session = requests.Session()
    retry_statuses = [requests.codes.too_many_requests,
                      requests.codes.internal_server_error,
                      requests.codes.bad_gateway,
                      requests.codes.service_unavailable,
                      requests.codes.gateway_timeout]
    retries = Retry(total=10, backoff_factor=1, status_forcelist=retry_statuses, method_whitelist=False)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


class Client(object):
    _session = _session_factory()

    @classmethod
    def clear_session(cls):
        cls._session = _session_factory()

    @classmethod
    def init_session(cls):
        if config.api_token_source:
            cls._session.headers["Authorization"] = "Bearer {}".format(config.api_token_source.token())
        elif "Authorization" not in cls._session.headers and config.api_token:
            cls._session.headers.update({"Authorization": "Bearer {}".format(config.api_token)})
        if cls._session.cert is None and config.cert:
            cls._session.cert = config.cert
        cls._session.verify = config.verify_ssl
        if not config.verify_ssl:
            import requests.packages.urllib3 as urllib3
            urllib3.disable_warnings()

    def get(self, url, timeout=config.timeout, **kwargs):
        return self._call("GET", url, timeout=timeout, **kwargs)

    def delete(self, url, timeout=config.timeout, **kwargs):
        return self._call("DELETE", url=url, timeout=timeout, **kwargs)

    def post(self, url, body, timeout=config.timeout):
        return self._call("POST", url, body, timeout=timeout)

    def put(self, url, body, timeout=config.timeout):
        return self._call("PUT", url, body, timeout=timeout)

    def _call(self, method, url, body=None, timeout=config.timeout, **kwargs):
        self.init_session()
        resp = self._session.request(method, config.api_server + url, json=body, timeout=timeout, **kwargs)
        if config.debug and not kwargs.get('stream', False):
            message = ['{:d} for url: {:s}'.format(resp.status_code, resp.url)]
            Client._add_request(message, resp.request)
            Client._add_response(message, resp)
            LOG.debug("\n".join(message))
        self._raise_on_status(resp)
        return resp

    @staticmethod
    def _raise_on_status(resp):
        if resp.status_code < 400:
            return
        elif resp.status_code == 404:
            exc = NotFound
        elif 400 <= resp.status_code < 500:
            exc = ClientError
        else:
            exc = ServerError
        http_error_msg = Client._build_error_message(resp)
        raise exc(http_error_msg, response=resp)

    @staticmethod
    def _build_error_message(resp):
        request = resp.request
        message = ['{:d}: {:s} for url: {:s}'.format(resp.status_code, resp.reason, resp.url)]
        Client._add_causes(message, resp)
        Client._add_request(message, request)
        Client._add_response(message, resp)
        return "\n".join(message)

    @staticmethod
    def _add_causes(message, resp):
        try:
            json_response = resp.json()
            json_causes = json_response.get(u"details", {}).get(u"causes", {})
            if json_causes:
                message.append("Causes:")
                message.extend("\t{}: {}".format(d[u"field"], d[u"message"]) for d in json_causes)
        except Exception as e:
            LOG.debug("Exception when dealing with client error response: %s", e)
            LOG.debug("Response: %r", resp.text)

    @staticmethod
    def _add_response(message, resp):
        message.append("Response:")
        Client._add_headers(message, resp.headers, "<<<")
        if resp.text:
            message.append("<<< ")
            message.extend("<<< {}".format(line) for line in resp.text.splitlines())

    @staticmethod
    def _add_request(message, request):
        message.append("Request:")
        message.append(">>> {method} {url}".format(method=request.method, url=request.url))
        Client._add_headers(message, request.headers, ">>>")
        if request.body:
            message.append(">>> ")
            message.extend(">>> {}".format(line) for line in request.body.splitlines())

    @staticmethod
    def _add_headers(message, headers, prefix):
        for key, value in headers.items():
            if key.lower() in SENSITIVE_HEADERS:
                value = "#REDACTED#"
            message.append("{} {}: {}".format(prefix, key, value))
