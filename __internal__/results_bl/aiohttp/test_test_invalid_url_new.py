import pytest
from aiohttp import web, InvalidURL
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

def test_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(InvalidURL):
        make_request("get", "hiwpefhipowhefopw")

def test_empty_path(make_request: _RequestMaker) -> None:
    with pytest.raises(InvalidURL):
        make_request("get", "")

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(InvalidURL):
        make_request("invalid_method", "http://example.com")

def test_missing_scheme(make_request: _RequestMaker) -> None:
    with pytest.raises(InvalidURL):
        make_request("get", "example.com/path")

def test_invalid_host(make_request: _RequestMaker) -> None:
    with pytest.raises(InvalidURL):
        make_request("get", "http://[::1]:80/path")

def test_protocols_header(make_request: _RequestMaker) -> None:
    request = make_request("get", "/path", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'Custom-Header': 'value'})
    request = make_request("get", "/path", headers=custom_headers)
    assert request.headers['Custom-Header'] == 'value'