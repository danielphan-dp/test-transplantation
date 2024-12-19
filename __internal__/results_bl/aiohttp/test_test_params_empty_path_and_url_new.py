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

def test_params_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req_with_headers = make_request("get", "http://python.org", headers=custom_headers)
    assert req_with_headers.headers['CUSTOM-HEADER'] == 'value'

def test_params_with_protocols(make_request: _RequestMaker) -> None:
    req_with_protocols = make_request("get", "http://python.org", protocols=True)
    assert req_with_protocols.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_params_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org")

def test_params_empty_headers(make_request: _RequestMaker) -> None:
    req_empty_headers = make_request("get", "http://python.org", headers=CIMultiDict())
    assert 'HOST' in req_empty_headers.headers
    assert req_empty_headers.headers['HOST'] == 'server.example.com'

def test_params_no_headers(make_request: _RequestMaker) -> None:
    req_no_headers = make_request("get", "http://python.org", headers=None)
    assert req_no_headers.headers['HOST'] == 'server.example.com'