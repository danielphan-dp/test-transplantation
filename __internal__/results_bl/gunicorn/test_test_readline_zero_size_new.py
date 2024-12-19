import io
import pytest
from gunicorn.http.body import Body

def test_readline_negative_size():
    with pytest.raises(ValueError):
        assert_readline(b"abc", -1, b"")

def test_readline_large_size():
    assert_readline(b"abc", 10, b"abc")

def test_readline_exact_size():
    assert_readline(b"abc", 3, b"abc")

def test_readline_with_newline():
    assert_readline(b"abc\nxyz", 4, b"abc\n")

def test_readline_empty_payload():
    assert_readline(b"", 5, b"")