import io
import pytest
from gunicorn.http.body import Body

def test_readline_non_empty_body():
    assert_readline(b"hello\nworld\n", None, b"hello\n")
    assert_readline(b"hello\nworld\n", 5, b"hello")
    assert_readline(b"hello\nworld\n", 10, b"hello\nworld")
    assert_readline(b"hello\nworld\n", 1, b"h")
    assert_readline(b"hello\nworld\n", 6, b"hello\n")

def test_readline_with_size_greater_than_line_length():
    assert_readline(b"short\nline\n", 10, b"short\n")
    assert_readline(b"singleline", 20, b"singleline")

def test_readline_with_zero_size():
    assert_readline(b"data\nmoredata\n", 0, b"")
    assert_readline(b"data\nmoredata\n", 0, b"")

def test_readline_with_exceeding_size():
    assert_readline(b"line1\nline2\nline3\n", 15, b"line1\n")
    assert_readline(b"line1\nline2\nline3\n", 20, b"line1\nline2\nline3\n")