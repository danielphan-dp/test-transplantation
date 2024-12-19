import pytest
from multidict import CIMultiDict
from aiohttp import web

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]]=None, protocols: bool=False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

def test_host_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/")

def test_host_missing_host_header(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade'})
    request = make_request("GET", "/", headers=headers)
    assert request.headers.get('HOST') is None

def test_host_invalid_upgrade_header(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'invalid_upgrade'})
    request = make_request("GET", "/", headers=headers)
    assert request.headers['UPGRADE'] == 'invalid_upgrade'

def test_host_invalid_port_format(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("GET", "http://python.org:abc/")

def test_host_with_custom_protocols(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade'})
    request = make_request("GET", "/", headers=headers, protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'