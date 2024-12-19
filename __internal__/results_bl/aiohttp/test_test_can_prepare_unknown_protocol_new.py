import asyncio
import time
from typing import Optional, Protocol
from unittest.mock import Mock
import aiosignal
import pytest
from multidict import CIMultiDict
from pytest_mock import MockerFixture
from aiohttp import WSMessageTypeError, WSMsgType, web
from aiohttp.http import WS_CLOSED_MESSAGE, WS_CLOSING_MESSAGE
from aiohttp.http_websocket import WSMessageClose
from aiohttp.streams import EofStream
from aiohttp.test_utils import make_mocked_coro, make_mocked_request
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

def test_can_prepare_with_valid_protocol(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    ws = web.WebSocketResponse()
    assert WebSocketReady(True, None) == ws.can_prepare(req)

def test_can_prepare_with_invalid_protocol(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=CIMultiDict({'SEC-WEBSOCKET-PROTOCOL': 'invalid_protocol'}))
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/")
    ws = web.WebSocketResponse()
    assert WebSocketReady(True, None) == ws.can_prepare(req)

def test_can_prepare_with_missing_upgrade_header(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'server.example.com', 'CONNECTION': 'Upgrade'})
    req = make_request("GET", "/", headers=headers)
    ws = web.WebSocketResponse()
    assert WebSocketReady(False, None) == ws.can_prepare(req)

def test_can_prepare_with_multiple_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    ws = web.WebSocketResponse()
    assert WebSocketReady(True, None) == ws.can_prepare(req)