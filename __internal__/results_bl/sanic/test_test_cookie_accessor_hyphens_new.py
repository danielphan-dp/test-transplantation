import pytest
from sanic.response import text
from sanic.cookies.request import CookieRequestParameters

def test_get_method_valid_request():
    request = Mock()
    response = get(request)
    assert response.body == b'I am get method'

def test_get_method_empty_request():
    request = Mock()
    request.args = {}
    response = get(request)
    assert response.body == b'I am get method'

def test_get_method_with_cookies():
    cookies = CookieRequestParameters({"session-token": ["abc123"]})
    request = Mock()
    request.cookies = cookies
    response = get(request)
    assert response.body == b'I am get method'

def test_get_method_invalid_request():
    request = Mock()
    request.args = None
    with pytest.raises(TypeError):
        get(request)