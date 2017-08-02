#!/usr/bin/env python
# -*- coding: utf-8

import os
from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


GENERIC_REQ = [
    "six == 1.10.0",
    "requests == 2.13.0"
]

FLAKE8_REQ = [
    'flake8-print',
    'flake8-comprehensions',
    'pep8-naming',
    'flake8'
]

TESTS_REQ = [
    'vcrpy',
    'mock',
    'pytest-sugar',
    'pytest-html',
    'pytest-cov',
    'pytest-helpers-namespace',
    'pytest >= 3.0'
]

setup(
    name="k8s",
    author="FINN Team Infrastructure",
    author_email="FINN-TechteamInfrastruktur@finn.no",
    version="1.0",
    packages=find_packages(exclude=("tests",)),
    zip_safe=True,
    include_package_data=True,

    # Requirements
    install_requires=GENERIC_REQ + FLAKE8_REQ,
    setup_requires=['pytest-runner', 'wheel', 'setuptools_git >= 0.3'],
    tests_require=TESTS_REQ,

    # Metadata
    description="Python client library for the Kubernetes API",
    long_description=read("README.md"),
    url="https://github.com/fiaas/k8s",
)
