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

def test_host_port_custom_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://custom.example.com:8080/")
    assert req.host == "custom.example.com"
    assert req.port == 8080
    assert not req.is_ssl()

def test_host_port_ssl_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'header.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "ws://header.example.com/", headers=headers)
    assert req.host == "header.example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://protocol.example.com/", protocols=True)
    assert req.host == "protocol.example.com"
    assert req.port == 80
    assert not req.is_ssl()
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'