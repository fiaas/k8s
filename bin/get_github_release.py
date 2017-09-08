#!/usr/bin/env python
# -*- coding: utf-8

"""Download the latest version of github-release and place in a temporary location"""

from __future__ import unicode_literals, print_function

import platform
import subprocess
import sys
import tempfile

import os
import re
import requests

URL = "https://api.github.com/repos/aktau/github-release/releases/latest"
ASSET_NAME_PATTERN = re.compile(r"^{}-amd64-github-release\.tar\.bz2$".format(platform.system().lower()))


def main():
    release_info = _get_release_info()
    asset_url = _find_wanted_asset(release_info)
    tmp_dir, asset_path = _download_asset(asset_url)
    bin_path = _unpack(tmp_dir, asset_path)
    print(bin_path)


def _unpack(tmp_dir, asset_path):
    output = subprocess.check_output(["tar", "--directory", tmp_dir, "-xjvf", asset_path])
    return os.path.join(tmp_dir, output.strip().decode(sys.getfilesystemencoding()))


def _download_asset(asset_url):
    resp = requests.get(asset_url)
    resp.raise_for_status()
    tmp_dir = tempfile.mkdtemp(prefix="github-release-")
    fpath = os.path.join(tmp_dir, "github-release")
    with open(fpath, "wb") as fobj:
        for chunk in resp.iter_content(chunk_size=8192):
            fobj.write(chunk)
    return tmp_dir, fpath


def _get_release_info():
    resp = requests.get(URL)
    resp.raise_for_status()
    release_info = resp.json()
    return release_info


def _find_wanted_asset(release_info):
    names = list()
    for asset in release_info["assets"]:
        name = asset["name"]
        names.append(name)
        m = ASSET_NAME_PATTERN.match(name)
        if m:
            return asset["browser_download_url"]
    raise RuntimeError("No asset in {} matches {!r}".format(
        ", ".join(names),
        ASSET_NAME_PATTERN.pattern
    ))


if __name__ == "__main__":
    main()
