#!/usr/bin/env python
# -*- coding: utf-8

import os
from setuptools import setup, find_packages

GENERIC_REQ = [
    "six == 1.10.0",
    "requests == 2.13.0"
]

CODE_QUALITY_REQ = [
    'prospector'
]

TESTS_REQ = [
    'tox==2.7.0',
    'vcrpy',
    'mock',
    'pytest-sugar',
    'pytest-html',
    'pytest-cov',
    'pytest-helpers-namespace',
    'pytest >= 3.0',
    'gitpython'
]


def _generate_description():
    description = [_read("README.md")]
    changelog_file = os.getenv("CHANGELOG_FILE")
    if changelog_file:
        description.append(_read(changelog_file))
    return "\n".join(description)


def _read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


def main():
    setup(
        name="k8s",
        author="FINN Team Infrastructure",
        author_email="FINN-TechteamInfrastruktur@finn.no",
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
            "release": ["gitpython", "twine"]
        },

        # Metadata
        description="Python client library for the Kubernetes API",
        long_description=_generate_description(),
        url="https://github.com/fiaas/k8s",
        license=_read("LICENSE")
    )


if __name__ == "__main__":
    main()
