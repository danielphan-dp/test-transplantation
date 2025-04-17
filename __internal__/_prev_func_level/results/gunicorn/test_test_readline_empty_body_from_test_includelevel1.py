import io
import pytest
from gunicorn.http.body import Body

def test_readline_with_size():
    assert_readline(b"hello\nworld\n", 5, b"hello")
    assert_readline(b"hello\nworld\n", 6, b"hello\n")
    assert_readline(b"hello\nworld\n", 10, b"hello\nworld")
    assert_readline(b"hello\nworld\n", None, b"hello\nworld\n")

def test_readline_with_partial_read():
    assert_readline(b"abc\ndef\n", 2, b"ab")
    assert_readline(b"abc\ndef\n", 4, b"abc\n")
    assert_readline(b"abc\ndef\n", 1, b"a")
    assert_readline(b"abc\ndef\n", 3, b"abc")

def test_readline_edge_cases():
    assert_readline(b"\n", None, b"\n")
    assert_readline(b"\n", 1, b"\n")
    assert_readline(b"\n", 0, b"")
    assert_readline(b"", 0, b"")
    assert_readline(b"", 1, b"")