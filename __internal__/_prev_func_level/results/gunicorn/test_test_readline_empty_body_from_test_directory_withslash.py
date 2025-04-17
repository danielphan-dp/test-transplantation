import io
import pytest
from gunicorn.http.body import Body

def test_readline_with_size():
    assert_readline(b"hello\nworld\n", 5, b"hello")
    assert_readline(b"hello\nworld\n", 10, b"hello\n")
    assert_readline(b"hello\nworld\n", 15, b"hello\nworld\n")

def test_readline_with_partial_size():
    assert_readline(b"hello\nworld\n", 3, b"hel")
    assert_readline(b"hello\nworld\n", 8, b"hello\nw")
    assert_readline(b"hello\nworld\n", 12, b"hello\nworld")

def test_readline_with_zero_size():
    assert_readline(b"hello\nworld\n", 0, b"")

def test_readline_with_exceeding_size():
    assert_readline(b"hello\nworld\n", 20, b"hello\nworld\n")

def test_readline_with_empty_payload():
    assert_readline(b"", None, b"")
    assert_readline(b"", 1, b"")