import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]]=None, protocols: bool=False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

def test_missing_auth_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org")
    assert "AUTHORIZATION" not in req.headers

def test_invalid_method(make_request: _RequestMaker) -> None:
    req = make_request("invalid_method", "http://python.org")
    assert req.method == "INVALID_METHOD"

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://python.org", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_websocket_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", protocols=True)
    assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_auth_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org", auth=aiohttp.BasicAuth("user!@#", "pass$%^"))
    assert "AUTHORIZATION" in req.headers
    assert req.headers["AUTHORIZATION"] == "Basic dXNlciFAIyE6cGFzJCUl"  # Base64 encoding of user!@#:pass$%^

def test_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == ""