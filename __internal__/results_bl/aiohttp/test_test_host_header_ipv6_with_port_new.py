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

def test_host_header_ipv6_without_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[::2]")
    assert req.headers["HOST"] == "[::2]"

def test_host_header_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "http://example.com", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"

def test_host_header_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com", headers=None)
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")