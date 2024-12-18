import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.mark.parametrize("method, path, headers, protocols", [
    ("GET", "/test", None, False),
    ("POST", "/test", CIMultiDict({"CUSTOM-HEADER": "value"}), True),
    ("PUT", "/test", CIMultiDict({"SEC-WEBSOCKET-PROTOCOL": "chat"}), False),
    ("DELETE", "/test", None, True),
])
def test_make_request_headers(make_request, method, path, headers, protocols):
    request = make_request(method, path, headers, protocols)
    assert request.method == method
    assert request.path == path
    if headers is None:
        assert request.headers['HOST'] == 'server.example.com'
        assert request.headers['UPGRADE'] == 'websocket'
        assert request.headers['CONNECTION'] == 'Upgrade'
        assert request.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
        assert request.headers['ORIGIN'] == 'http://example.com'
        assert request.headers['SEC-WEBSOCKET-VERSION'] == '13'
    else:
        for key, value in headers.items():
            assert request.headers[key] == value
    if protocols:
        assert 'SEC-WEBSOCKET-PROTOCOL' in request.headers
    else:
        assert 'SEC-WEBSOCKET-PROTOCOL' not in request.headers

def test_make_request_invalid_method(make_request):
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/test")