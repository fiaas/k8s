#!/usr/bin/env python
# -*- coding: utf-8


def _Enum(name, attrs):
    return type(name, (object,), {a: a for a in attrs})


ResourceQuotaScope = _Enum("ResourceQuota", (
    "Terminating",
    "NotTerminating",
    "BestEffort",
    "NotBestEffort",
))
