#!/usr/bin/env python
# -*- coding: utf-8

import subprocess

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
    'pytest >= 3.0'
]


def _has_tags():
    """setuptools_git will crash if you ask it to use vcs version without any tags in the repo"""
    try:
        subprocess.check_output(["git", "describe"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    return True


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
        use_vcs_version=_has_tags(),
        packages=find_packages(exclude=("tests",)),
        zip_safe=True,
        include_package_data=True,

        # Requirements
        install_requires=GENERIC_REQ,
        setup_requires=['pytest-runner', 'wheel', 'setuptools_git >= 1.2'],
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
