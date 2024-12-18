import pytest
from aiohttp.http_parser import HttpRequestParser

@pytest.mark.parametrize("encoding, expected", [
    ("utf-8", "Hello, World!"),
    ("ascii", "Hello, World!"),
    ("latin1", "Hello, World!"),
    ("invalid-encoding", "Hello, World!"),
])
def test_decode_method(parser: HttpRequestParser, encoding: str, expected: str) -> None:
    if encoding == "invalid-encoding":
        with pytest.raises(UnicodeDecodeError):
            parser.decode(encoding=encoding)
    else:
        result = parser.decode(encoding=encoding)
        assert result == expected

def test_decode_empty_string(parser: HttpRequestParser) -> None:
    result = parser.decode(encoding="utf-8")
    assert result == ""

def test_decode_non_utf8_bytes(parser: HttpRequestParser) -> None:
    non_utf8_bytes = b'\xff\xfeH\x00e\x00l\x00l\x00o\x00'
    result = parser.decode(encoding="utf-16")
    assert result == "Hello"