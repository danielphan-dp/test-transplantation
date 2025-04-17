import pytest
from aiohttp.http_parser import HttpRequestParser

@pytest.mark.parametrize("encoding, expected", [
    ("utf-8", "Hello, world!"),
    ("latin1", "Hello, world!"),
    ("ascii", "Hello, world!"),
    ("invalid-encoding", "Hello, world!"),
])
def test_decode_with_various_encodings(encoding, expected):
    parser = HttpRequestParser()
    data = expected.encode(encoding)
    result = parser.decode(encoding=encoding)
    assert result == expected

def test_decode_with_empty_string():
    parser = HttpRequestParser()
    result = parser.decode(encoding='utf-8')
    assert result == ""

def test_decode_with_non_utf8_bytes():
    parser = HttpRequestParser()
    data = b'\xff\xfeH\x00e\x00l\x00l\x00o\x00'
    result = parser.decode(encoding='utf-16')
    assert result == "Hello"

def test_decode_with_invalid_encoding():
    parser = HttpRequestParser()
    with pytest.raises(LookupError):
        parser.decode(encoding='invalid-encoding')