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

def test_headers_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_headers_without_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=False)
    assert "SEC-WEBSOCKET-PROTOCOL" not in req.headers

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"CUSTOM-HEADER": "custom_value"}
    req = make_request("get", "http://python.org/", headers=custom_headers)
    assert req.headers["CUSTOM-HEADER"] == "custom_value"

def test_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert req.headers["ORIGIN"] == "http://example.com"
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"