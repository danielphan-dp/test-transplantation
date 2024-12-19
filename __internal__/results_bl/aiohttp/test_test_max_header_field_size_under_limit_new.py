import pytest
from aiohttp.http_parser import HttpRequestParser

@pytest.fixture
def parser():
    return HttpRequestParser()

def test_decode_with_default_encoding(parser):
    result = parser.decode()
    assert isinstance(result, str)
    assert result == ''

def test_decode_with_utf8_encoding(parser):
    result = parser.decode(encoding='utf-8')
    assert isinstance(result, str)

def test_decode_with_invalid_encoding(parser):
    with pytest.raises(LookupError):
        parser.decode(encoding='invalid-encoding')

def test_decode_with_strict_errors(parser):
    result = parser.decode(errors='strict')
    assert isinstance(result, str)

def test_decode_with_ignore_errors(parser):
    result = parser.decode(errors='ignore')
    assert isinstance(result, str)

def test_decode_with_replace_errors(parser):
    result = parser.decode(errors='replace')
    assert isinstance(result, str)

def test_decode_with_non_string_input(parser):
    with pytest.raises(TypeError):
        parser.decode(encoding=123)

def test_decode_with_large_input(parser):
    large_input = 'a' * 10000
    result = parser.decode(encoding='utf-8', errors='strict')
    assert isinstance(result, str)
    assert len(result) == 10000

def test_decode_with_empty_string(parser):
    result = parser.decode(encoding='', errors='strict')
    assert result == ''