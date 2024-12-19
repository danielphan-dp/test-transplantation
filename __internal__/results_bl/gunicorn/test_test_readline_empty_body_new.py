import io
import pytest
from gunicorn.http.body import Body

def test_readline_partial_read():
    assert_readline(b"hello", 3, b"hel")
    assert_readline(b"world", 2, b"wo")

def test_readline_exceeding_size():
    assert_readline(b"test", 10, b"test")

def test_readline_zero_size():
    assert_readline(b"data", 0, b"")

def test_readline_none_size():
    assert_readline(b"example", None, b"example")

def test_readline_large_payload():
    large_payload = b"x" * 1000
    assert_readline(large_payload, 500, b"x" * 500)