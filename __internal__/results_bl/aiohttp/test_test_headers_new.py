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

def test_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"X-Custom-Header": "CustomValue"}
    req = make_request("post", "http://python.org/", headers=custom_headers)
    assert "X-CUSTOM-HEADER" in req.headers
    assert req.headers["X-CUSTOM-HEADER"] == "CustomValue"

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")

def test_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == ""