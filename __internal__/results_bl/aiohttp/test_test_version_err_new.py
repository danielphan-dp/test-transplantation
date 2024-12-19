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

def test_make_request_with_default_headers(make_request: _RequestMaker, app: web.Application) -> None:
    request = make_request("GET", "/test")
    assert request.headers['HOST'] == 'server.example.com'
    assert request.headers['UPGRADE'] == 'websocket'

def test_make_request_with_custom_headers(make_request: _RequestMaker, app: web.Application) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    request = make_request("POST", "/test", headers=custom_headers)
    assert request.headers['CUSTOM-HEADER'] == 'value'

def test_make_request_with_protocols(make_request: _RequestMaker, app: web.Application) -> None:
    request = make_request("GET", "/test", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_with_invalid_method(make_request: _RequestMaker, app: web.Application) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/test")

def test_make_request_with_empty_path(make_request: _RequestMaker, app: web.Application) -> None:
    with pytest.raises(ValueError):
        make_request("GET", "")