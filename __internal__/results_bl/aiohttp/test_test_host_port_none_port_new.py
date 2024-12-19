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

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "/path", headers=custom_headers)
    assert req.headers["Host"] == "custom.example.com"

def test_host_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", headers=None)
    assert req.headers["Host"] == "server.example.com"

def test_host_with_invalid_method(make_request: _RequestMaker) -> None:
    req = make_request("invalid_method", "/path")
    assert req.method == "INVALID_METHOD"

def test_host_with_websocket_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == ""