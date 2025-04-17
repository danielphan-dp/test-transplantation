import io
import pytest
from gunicorn.http.body import Body

def test_readline_non_zero_size():
    assert_readline(b"abc\n", 1, b"a")
    assert_readline(b"abc\n", 2, b"ab")
    assert_readline(b"abc\n", 3, b"abc")
    assert_readline(b"abc\n", 4, b"abc\n")

def test_readline_exceeding_size():
    assert_readline(b"abc\n", 10, b"abc\n")
    assert_readline(b"abc\nxyz\n", 10, b"abc\nxyz\n")

def test_readline_empty_payload():
    assert_readline(b"", 1, b"")
    assert_readline(b"", 0, b"")

def test_readline_with_multiple_lines():
    assert_readline(b"line1\nline2\nline3\n", 5, b"line1")
    assert_readline(b"line1\nline2\nline3\n", 10, b"line1\nline2")
    assert_readline(b"line1\nline2\nline3\n", 15, b"line1\nline2\nline3\n")