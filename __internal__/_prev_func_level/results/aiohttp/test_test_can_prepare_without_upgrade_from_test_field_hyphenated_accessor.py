import pytest
from aiohttp import web
from multidict import CIMultiDict
from aiohttp.web_ws import WebSocketReady

@pytest.fixture
def make_request(app: web.Application, protocol: web.RequestHandler[web.Request]) -> _RequestMaker:
    def maker(method: str, path: str, headers: Optional[CIMultiDict[str]] = None, protocols: bool = False) -> web.Request:
        if headers is None:
            headers = CIMultiDict({'HOST': 'server.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade', 'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==', 'ORIGIN': 'http://example.com', 'SEC-WEBSOCKET-VERSION': '13'})
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers, app=app, protocol=protocol)
    return maker

def test_can_prepare_with_upgrade(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=CIMultiDict({'UPGRADE': 'websocket'}))
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket', 'CONNECTION': 'Upgrade'})
    req = make_request("GET", "/", headers=custom_headers)
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/")
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_invalid_method(make_request: _RequestMaker) -> None:
    req = make_request("POST", "/")
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)  # Expecting it to handle non-GET gracefully

def test_can_prepare_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)