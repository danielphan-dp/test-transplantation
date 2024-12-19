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

def test_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://test.com/path", headers={})
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    req = make_request("get", "http://test.com/path", headers=custom_headers)
    assert "CUSTOM-HEADER" in req.headers
    assert req.headers["CUSTOM-HEADER"] == "custom_value"

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://test.com/path", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://test.com/path")

def test_special_characters_in_headers(make_request: _RequestMaker) -> None:
    special_headers = CIMultiDict({'SPECIAL-CHAR': 'value/with/special&chars'})
    req = make_request("get", "http://test.com/path", headers=special_headers)
    assert "SPECIAL-CHAR" in req.headers
    assert req.headers["SPECIAL-CHAR"] == "value/with/special&chars"