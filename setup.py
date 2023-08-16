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


import os

from setuptools import setup, find_packages

GENERIC_REQ = [
    "requests==2.31.0",
    "pyrfc3339==1.1",
    "cachetools==3.1.1",  # Newer versions require Python 3
]

CODE_QUALITY_REQ = [
    'prospector==1.2.0',  # Newer versions require Python 3
]

TESTS_REQ = [
    'tox==3.24.5',
    'mock==3.0.5',  # Newer versions require Python 3
    "pytest-sugar==0.9.4",
    "pytest-html==1.22.0",  # Newer versions require Python 3
    "pytest-cov==2.7.1",
    "pytest-helpers-namespace==2019.1.8",
    'pytest==4.6.11',  # Newer versions require Python 3
]


def _generate_description():
    description = [_read("README.rst")]
    changelog_file = os.getenv("CHANGELOG_FILE")
    if changelog_file:
        description.append(_read(changelog_file))
    return "\n".join(description)


def _get_license_name():
    with open(os.path.join(os.path.dirname(__file__), "LICENSE")) as f:
        for line in f:
            if line.strip():
                return line.strip()


def _read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


def main():
    setup(
        name="k8s",
        author="FiaaS developers",
        author_email="fiaas@googlegroups.com",
        use_scm_version=True,
        packages=find_packages(exclude=("tests",)),
        zip_safe=True,
        include_package_data=True,

        # Requirements
        install_requires=GENERIC_REQ,
        setup_requires=['pytest-runner', 'wheel', 'setuptools_scm'],
        extras_require={
            "dev": TESTS_REQ + CODE_QUALITY_REQ,
            "codacy": ["codacy-coverage"],
            "docs": ["Sphinx>=1.6.3"]
        },
        tests_require=TESTS_REQ,
        # Metadata
        description="Python client library for the Kubernetes API",
        long_description=_generate_description(),
        url="https://github.com/fiaas/k8s",
        license=_get_license_name(),
        keywords="kubernetes fiaas",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Clustering",
            "Topic :: System :: Distributed Computing",
        ]
    )


if __name__ == "__main__":
    main()
