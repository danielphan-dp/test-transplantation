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

def test_path_with_special_chars(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/!@#$%^&*()")
    assert req.url.path == "/get/!@#$%^&*()"

def test_path_with_empty_string(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/")
    assert req.url.path == "/get/"

def test_path_with_query_string(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/?query=1")
    assert req.url.path == "/get/"

def test_path_with_encoded_chars(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/%20space%20")
    assert req.url.path == "/get/ space "

def test_path_with_long_path(make_request: _RequestMaker) -> None:
    long_path = "http://0.0.0.0/get/" + "a" * 2000
    req = make_request("get", long_path)
    assert req.url.path == "/get/" + "a" * 2000

def test_path_with_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'