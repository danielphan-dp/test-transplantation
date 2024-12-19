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

def test_ipv6_custom_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]:8080/")
    assert req.host == "2001:db8::1"
    assert req.port == 8080
    assert req.is_ssl()

def test_ipv6_no_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]")
    assert req.host == "2001:db8::1"
    assert req.port == 443
    assert req.is_ssl()

def test_ipv6_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "https://[invalid::url]/")

def test_ipv6_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "https://[2001:db8::1]/", headers=headers)
    assert req.headers['HOST'] == 'custom.example.com'
    assert req.host == "2001:db8::1"
    assert req.port == 443
    assert req.is_ssl()

def test_ipv6_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'
    assert req.host == "2001:db8::1"
    assert req.port == 443
    assert req.is_ssl()