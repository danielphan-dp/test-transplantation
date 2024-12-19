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

def test_ipv6_default_https_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]/")
    assert req.host == "2001:db8::1"
    assert req.port == 443
    assert req.is_ssl()

def test_ipv6_nondefault_http_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[2001:db8::1]:8080/")
    assert req.host == "2001:db8::1"
    assert req.port == 8080
    assert not req.is_ssl()

def test_invalid_ipv6_address(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "http://[invalid::address]/")

def test_websocket_upgrade_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://[2001:db8::1]/", protocols=True)
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'
    assert 'SEC-WEBSOCKET-PROTOCOL' in req.headers

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://example.com/", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'