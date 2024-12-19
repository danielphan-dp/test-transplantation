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

def test_host_port_default_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://localhost:80/")
    assert req.host == "localhost"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_ssl_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://secure.example.com:443/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_invalid_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://invalid_host:9999/")
    assert req.host == "invalid_host"
    assert req.port == 9999
    assert not req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "ws://custom.example.com:8080/", headers=headers)
    assert req.host == "custom.example.com"
    assert req.port == 8080
    assert not req.is_ssl()