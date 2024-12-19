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

def test_host_port_default_http(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/")
    assert req.host == "example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_query_params(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org:960/?query=param")
    assert req.host == "python.org"
    assert req.port == 960
    assert not req.is_ssl()

def test_host_with_invalid_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org:99999/")
    assert req.host == "python.org"
    assert req.port == 99999  # This should be handled by the application logic

def test_host_with_no_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.host == "python.org"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://python.org/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'