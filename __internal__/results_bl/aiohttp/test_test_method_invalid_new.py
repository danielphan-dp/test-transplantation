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

def test_method_empty(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("", "http://python.org/")

def test_method_invalid_characters(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request("GET@", "http://python.org/")

def test_method_long_string(make_request: _RequestMaker) -> None:
    long_method = "A" * 300
    with pytest.raises(ValueError, match="Method cannot contain non-token characters"):
        make_request(long_method, "http://python.org/")

def test_method_valid(make_request: _RequestMaker) -> None:
    request = make_request("GET", "http://python.org/")
    assert request.method == "GET"

def test_method_with_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'Custom-Header': 'Value'})
    request = make_request("GET", "http://python.org/", headers=headers)
    assert request.headers['Custom-Header'] == 'Value'