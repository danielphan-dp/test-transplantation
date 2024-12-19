import pytest
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_invalid_encoding() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("invalid_encoding", errors='strict')

def test_basic_auth_decode_invalid_errors() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode(encoding='utf-8', errors='invalid_error_handling')

def test_basic_auth_decode_empty_string() -> None:
    result = BasicAuth.decode("")
    assert result == ""

def test_basic_auth_decode_none_encoding() -> None:
    with pytest.raises(TypeError):
        BasicAuth.decode(None)

def test_basic_auth_decode_none_errors() -> None:
    with pytest.raises(TypeError):
        BasicAuth.decode(encoding='utf-8', errors=None)