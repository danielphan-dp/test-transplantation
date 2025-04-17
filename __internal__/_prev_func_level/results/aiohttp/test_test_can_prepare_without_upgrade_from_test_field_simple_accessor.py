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

def test_can_prepare_with_upgrade(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=CIMultiDict({'UPGRADE': 'websocket'}))
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
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
    assert WebSocketReady(False, None) == ws.can_prepare(req)