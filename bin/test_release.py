from __future__ import unicode_literals

import argparse

import mock
import pytest
from git import Repo, TagObject, Commit, GitCommandError
from git.util import hex_to_bin

import release

PREVIOUS_TAG = "v1.2.2"
CURRENT_TAG = "v1.2.3"


def _h2b(prefix):
    return hex_to_bin(_pad(prefix))


def _pad(prefix):
    return prefix + "0" * (40 - len(prefix))


class TestRepository(object):
    @pytest.fixture
    def options(self):
        return argparse.Namespace(directory=".", dry_run=True, force=False)

    @pytest.fixture
    def git_repo(self):
        with mock.patch("release.Repo", spec=Repo, spec_set=True) as mock_repo:
            commits = [
                Commit(mock_repo, _h2b("111111"), message="First commit", parents=tuple()),
                Commit(mock_repo, _h2b("222222"), message="Second commit", parents=("111111",)),
                Commit(mock_repo, _h2b("333333"), message="Third commit", parents=("222222",))
            ]
            mock_repo.iter_commits.return_value = commits
            rev_parse_returns = {
                "heads/master": commits[-1],
                PREVIOUS_TAG: TagObject(mock_repo, _h2b("aaaaaa"), object=commits[-2], tag=PREVIOUS_TAG),
                CURRENT_TAG: TagObject(mock_repo, _h2b("bbbbbb"), object=commits[-1], tag=CURRENT_TAG)
            }
            mock_repo.rev_parse.side_effect = lambda x: rev_parse_returns[x]
            mock_repo.git.rev_parse.side_effect = lambda x, **kwargs: x

            def describe(rev=None, **kwargs):
                print("call to describe(%r, %r)" % (rev, kwargs))
                if rev is None:
                    return CURRENT_TAG
                if rev.endswith("^"):
                    if rev.startswith(CURRENT_TAG):
                        return PREVIOUS_TAG
                    raise GitCommandError("describe", "failed")
                raise AssertionError("Test wants to describe something unexpected: rev=%r, kwargs=%r" % (rev, kwargs))

            mock_repo.git.describe.side_effect = describe
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

    @pytest.mark.parametrize("current_tag,previous_tag", (
        ("444444", release.THE_NULL_COMMIT),
        ("v1.2.3", "v1.2.2")
    ))
    def test_creates_changelog(self, monkeypatch, repository, git_repo, current_tag, previous_tag):
        monkeypatch.setattr(repository, "_current_tag", current_tag)
        changelog = repository.generate_changelog()

        assert len(changelog) == 3
        assert changelog[0] == (_pad("111111"), "First commit")
        assert changelog[1] == (_pad("222222"), "Second commit")
        assert changelog[2] == (_pad("333333"), "Third commit")

        git_repo.iter_commits.assert_called_with("{}..{}".format(previous_tag, current_tag))
