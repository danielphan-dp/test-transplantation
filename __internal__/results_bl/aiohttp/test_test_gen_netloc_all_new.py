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

def test_gen_netloc_empty_host(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert req.headers["HOST"] == "server.example.com"

def test_gen_netloc_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "/", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"

def test_gen_netloc_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_gen_netloc_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/")

def test_gen_netloc_long_host(make_request: _RequestMaker) -> None:
    long_host = "a" * 256
    req = make_request("get", f"https://{long_host}/")
    assert req.headers["HOST"] == long_host

def test_gen_netloc_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", headers=None)
    assert req.headers["HOST"] == "server.example.com"