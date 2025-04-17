import io
import pytest
from gunicorn.http.body import Body

def test_readline_non_empty_body():
    assert_readline(b"hello\nworld\n", None, b"hello\n")
    assert_readline(b"hello\nworld\n", 5, b"hello")
    assert_readline(b"hello\nworld\n", 10, b"hello\nworld")
    assert_readline(b"hello\nworld\n", 1, b"h")
    assert_readline(b"hello\nworld\n", 6, b"hello\n")
    assert_readline(b"hello\nworld\n", 15, b"hello\nworld\n")

def test_readline_with_size_zero():
    assert_readline(b"test\nline\n", 0, b"")
    assert_readline(b"test\nline\n", 0, b"")

def test_readline_exceeding_size():
    assert_readline(b"short\n", 10, b"short\n")
    assert_readline(b"another test\n", 20, b"another test\n")