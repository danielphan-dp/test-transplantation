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

def test_host_port_default_wss(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://python.org/")
    assert req.host == "python.org"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_http(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/")
    assert req.host == "example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com:8080/")
    assert req.host == "example.com"
    assert req.port == 8080
    assert not req.is_ssl()

def test_host_with_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")

def test_host_with_websocket_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://python.org/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'