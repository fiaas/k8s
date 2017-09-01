from __future__ import unicode_literals

import argparse

import mock
import pytest
from git import Repo, TagObject, Commit

import release


class TestRepository(object):
    @pytest.fixture
    def options(self):
        return argparse.Namespace(directory=".", dry_run=True, force=False)

    @pytest.fixture
    def git_repo(self):
        rev_parse_returns = {
            "heads/master": mock.NonCallableMagicMock(spec=Commit, name="master-commit", hexsha="abcdef"),
            "v1.2.2": mock.NonCallableMagicMock(spec=TagObject, name="122-tag", tag="v1.2.2"),
            "v1.2.3": mock.NonCallableMagicMock(spec=TagObject, name="123-tag", tag="v1.2.3")
        }
        with mock.patch("release.Repo", spec=Repo, spec_set=True) as mock_repo:
            mock_repo.git.describe.return_value = "v1.2.3"
            mock_repo.rev_parse.side_effect = lambda x: rev_parse_returns[x]
            yield mock_repo

    @pytest.fixture
    def repository(self, git_repo, options):
        repository = release.Repository(options)
        repository.repo = git_repo
        yield repository

    @pytest.mark.parametrize("dirty,untracked,result", (
            (True, True, False),
            (True, False, False),
            (False, True, False),
            (False, False, True)
    ))
    def test_can_not_release_from_unclean_repo(self, repository, git_repo, dirty, untracked, result):
        git_repo.is_dirty.return_value = dirty
        git_repo.untracked_files = ["a"] if untracked else []

        assert repository.ready_for_release() is result

    @pytest.mark.parametrize("name,result", (
            ("v1", True),
            ("v1.2", True),
            ("v1.2.3", True),
            ("v123", True),
            ("1.2.3", False),
            ("a.b.c", False),
            ("v1.a.3", False),
    ))
    def test_tag_must_match_version(self, repository, git_repo, name, result):
        git_repo.is_dirty.return_value = False
        git_repo.untracked_files = []
        git_repo.head.commit = "123"
        mock_tag = mock.MagicMock()
        mock_tag.tag = name
        git_repo.rev_parse.return_value = mock_tag
        git_repo.rev_parse.side_effect = None

        assert repository.ready_for_release() is result

    def test_creates_changelog(self, repository, git_repo):
        git_repo.iter_commits.return_value = [
            mock.NonCallableMagicMock(spec=Commit, hexsha="123456", summary="First commit"),
            mock.NonCallableMagicMock(spec=Commit, hexsha="abcdef", summary="Second commit")
        ]
        changelog = repository.generate_changelog()

        assert len(changelog) == 2
        assert changelog[0] == "123456 First commit"
        assert changelog[1] == "abcdef Second commit"

    def test_creates_changelog_since_initial_if_no_tag(self, repository, git_repo):
        git_repo.iter_commits.return_value = [
            mock.NonCallableMagicMock(spec=Commit, hexsha="123456", summary="First commit"),
            mock.NonCallableMagicMock(spec=Commit, hexsha="abcdef", summary="Second commit")
        ]
        git_repo.git.describe.return_value = "heads/master"
        changelog = repository.generate_changelog()

        assert len(changelog) == 2
        assert changelog[0] == "123456 First commit"
        assert changelog[1] == "abcdef Second commit"
