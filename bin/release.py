#!/usr/bin/env python
# -*- coding: utf-8

"""Release a new version of the k8s library

Script is assumed to be run using Semaphore CI to release a version from a
successful build.

To release a new version, create a git annotated tag named v<major>.<minor>.<patch>,
according to Semantic Versioning principles. After you have pushed the tag, CI will
build the commit, and then run this script to deploy a release.

The script will do the following steps:
- Check if the build refers exactly to an annotated tag following the convention above
- Generate a suitable changelog
- Create packages for upload (wheels and tarballs)
- Use https://github.com/aktau/github-release to create a Github release
- Use the projects setup.py to create a PyPi release
"""
from __future__ import unicode_literals, print_function

import argparse
import subprocess
import tempfile

import os
import re
from git import Repo, BadName, GitCommandError
from git.cmd import Git

# Magical, always present, empty tree reference
# https://stackoverflow.com/questions/9765453/
THE_NULL_COMMIT = Git().hash_object(os.devnull, t="tree")


class Formatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


class Repository(object):
    RELEASE_TAG_PATTERN = re.compile(r"^v\d+(\.\d+){0,2}$")

    def __init__(self, options):
        self.repo = Repo(options.directory)
        self._force = options.force
        self._current_tag = None

    @property
    def current_tag(self):
        if self._current_tag:
            return self._current_tag
        try:
            current_name = self.repo.git.describe(all=True)
            self._current_tag = self.repo.rev_parse(current_name)
            return self._current_tag
        except BadName:
            return None

    def ready_for_release(self):
        """Return true if the current git checkout is suitable for release

        To be suitable, it must not be dirty, must not have untracked files, must be an annotated tag,
        and the tag must follow the naming convention v<major>.<minor>.<bugfix>
        """
        if self._force:
            return True
        if self.repo.is_dirty() or self.repo.untracked_files or not self.current_tag:
            return False
        return self.RELEASE_TAG_PATTERN.match(self.current_tag.tag) is not None

    def generate_changelog(self):
        """Use the git log to create a changelog with all changes since the previous tag"""
        try:
            previous_name = self.repo.git.describe("{}^".format(self.current_tag), abbrev=0)
            previous_tag = self.repo.rev_parse(previous_name)
        except GitCommandError:
            previous_tag = THE_NULL_COMMIT
        commits = list(self.repo.iter_commits("{}..{}".format(previous_tag, self.current_tag)))
        return ["{} {}".format(commit.hexsha, commit.summary) for commit in commits]


def format_rst_changelog(changelog):
    return "\n".join(changelog)


def create_artifacts(changelog):
    """List all artifacts for uploads

    Wheels and tarballs
    """
    fd, name = tempfile.mkstemp(prefix="changelog", suffix=".rst", text=True)
    with os.fdopen(fd, "w") as fobj:
        fobj.write(format_rst_changelog(changelog))
    subprocess.check_call(["python", "setup.py", "sdist", "bdist_wheel", "--universal"], env={"CHANGELOG_FILE": name})
    return [os.path.abspath(os.path.join("dist", fname)) for fname in os.listdir("dist")]


def github_release(changelog, artifacts):
    """Create release in github.com, and upload artifacts and changelog"""
    pass


def pypi_release(artifacts):
    """Create release in pypi.python.org, and upload artifacts and changelog"""
    pass


def main(options):
    repo = Repository(options)
    if not repo.ready_for_release():
        print("Repository is not ready for release")
        return
    changelog = repo.generate_changelog()
    artifacts = create_artifacts(changelog)
    print("==== Ready to create release ====")
    print("---- Changelog ----")
    print("\n".join(changelog))
    print("---- Artifacts ----")
    print("\n".join(artifacts))
    print("-" * 40)
    github_release(changelog, artifacts)
    pypi_release(artifacts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=Formatter)
    parser.add_argument("-d", "--directory", default=".", help="Git repository")
    parser.add_argument("-f", "--force", action="store_true", help="Make a release even if the repo is unclean")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Do everything, except upload to GH/PyPI")
    options = parser.parse_args()
    main(options)
