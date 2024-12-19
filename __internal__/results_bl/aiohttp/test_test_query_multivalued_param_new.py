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

def test_make_request_with_default_headers(make_request: _RequestMaker) -> None:
    req = make_request('GET', 'http://example.com')
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request('POST', 'http://example.com', headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request('GET', 'http://example.com', protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request('GET', '')
    assert str(req.url) == 'http://server.example.com/'

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request('INVALID_METHOD', 'http://example.com')