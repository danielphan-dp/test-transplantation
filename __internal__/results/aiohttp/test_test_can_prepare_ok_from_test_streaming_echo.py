import pytest
from aiohttp import web
from multidict import CIMultiDict
from aiohttp.web_ws import WebSocketReady

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    ret: web.Application = mock.create_autospec(web.Application, spec_set=True)
    ret.on_response_prepare = aiosignal.Signal(ret)
    ret.on_response_prepare.freeze()
    return ret

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    ret.set_parser.return_value = ret
    return ret

def test_can_prepare_with_different_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    ws = web.WebSocketResponse(protocols=("chat", "superchat"))
    assert WebSocketReady(True, "chat") == ws.can_prepare(req)

def test_can_prepare_without_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=False)
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_invalid_protocol(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    ws = web.WebSocketResponse(protocols=("invalid_protocol",))
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("GET", "/", headers=custom_headers, protocols=True)
    ws = web.WebSocketResponse(protocols=("chat",))
    assert WebSocketReady(True, "chat") == ws.can_prepare(req)

def test_can_prepare_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=None, protocols=True)
    ws = web.WebSocketResponse(protocols=("chat",))
    assert WebSocketReady(True, "chat") == ws.can_prepare(req)