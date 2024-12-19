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

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://python.org/")
    assert req.host == "python.org"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org:8080/")
    assert req.host == "python.org"
    assert req.port == 8080
    assert not req.is_ssl()

def test_host_with_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")

def test_host_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    assert req.host == "python.org"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_websocket_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade'})
    req = make_request("get", "http://python.org/", headers=headers, protocols=True)
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'