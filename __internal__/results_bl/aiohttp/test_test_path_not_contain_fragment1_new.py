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

def test_path_with_query_string(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path?query=1")
    assert req.url.path == "/path"

def test_path_with_empty_fragment(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path#")
    assert req.url.path == "/path"

def test_path_with_no_fragment(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path")
    assert req.url.path == "/path"

def test_path_with_multiple_fragments(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path#fragment1#fragment2")
    assert req.url.path == "/path"

def test_path_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path%20with%20spaces")
    assert req.url.path == "/path with spaces"