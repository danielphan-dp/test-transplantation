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

def test_params_are_added_with_empty_query(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?a=b"

def test_params_are_added_with_no_params(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path")
    assert str(req.url) == "http://example.com/path"

def test_params_are_added_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?key=value#fragment", params={"a": "b c", "d": "e&f"})
    assert str(req.url) == "http://example.com/path?key=value&a=b%20c&d=e%26f"

def test_params_are_added_with_existing_params(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?existing=value", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?existing=value&a=b"

def test_params_are_added_with_fragment(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path#fragment", params={"a": "b"})
    assert str(req.url) == "http://example.com/path?a=b#fragment"