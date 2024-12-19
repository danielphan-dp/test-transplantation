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

def test_default_headers_no_custom_useragent(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    
    assert "USER-Agent" in req.headers
    assert req.headers["User-Agent"] == "aiohttp"

def test_default_headers_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"X-Custom-Header": "CustomValue"}
    req = make_request("get", "http://python.org/", headers=custom_headers)
    
    assert "X-Custom-Header" in req.headers
    assert req.headers["X-Custom-Header"] == "CustomValue"

def test_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "http://python.org/")