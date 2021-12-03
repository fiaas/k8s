from datetime import datetime, timedelta

import pytest

from k8s.config import FileTokenSource


# pylint: disable=R0201
class TestFileTokenSource(object):

    @pytest.fixture
    def token_file(self, tmpdir_factory):
        fpath = tmpdir_factory.mktemp(self.__class__.__name__).join('token_file')
        try:
            yield fpath
        finally:
            if fpath.exists():
                fpath.remove()

    def test_token_read(self, token_file):
        token = "secret token"  # nosec
        token_file.write(token)
        token_source = FileTokenSource(token_file=str(token_file))

        assert token_source.token() == token

    def test_token_re_read_after_expiry(self, token_file):
        initial_token = "secret token 1"  # nosec
        token_file.write(initial_token)
        initial_time = datetime(2021, 1, 1, 10, 10)

        token_source = FileTokenSource(token_file=str(token_file), now_func=lambda: initial_time)

        assert token_source.token(now_func=lambda: initial_time) == initial_token

        updated_token = "secret token 2"  # nosec
        token_file.write(updated_token)

        assert token_source.token(now_func=lambda: initial_time + timedelta(seconds=30)) == initial_token
        assert token_source.token(now_func=lambda: initial_time + timedelta(minutes=2)) == updated_token

    def test_token_raise_if_file_does_not_exist(self, token_file):
        with pytest.raises(IOError):
            FileTokenSource(token_file=str(token_file))
