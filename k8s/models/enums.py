#!/usr/bin/env python
# -*- coding: utf-8


def _make_enum(name, attrs):
    return type(name, (object,), {a: a for a in attrs})


ResourceQuotaScope = _make_enum("ResourceQuotaScope", (
    "Terminating",
    "NotTerminating",
    "BestEffort",
    "NotBestEffort",
))
