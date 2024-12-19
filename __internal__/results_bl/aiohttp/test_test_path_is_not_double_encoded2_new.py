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

def test_path_is_double_encoded(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test%252Fcase")
    assert req.url.raw_path == "/get/test%252Fcase"

def test_path_with_no_encoding(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test/case")
    assert req.url.raw_path == "/get/test/case"

def test_path_with_special_characters(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test%20case")
    assert req.url.raw_path == "/get/test%20case"

def test_path_with_empty_string(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/")
    assert req.url.raw_path == "/get/"

def test_path_with_query_parameters(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test?param=value")
    assert req.url.raw_path == "/get/test"