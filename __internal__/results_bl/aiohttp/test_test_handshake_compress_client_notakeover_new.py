import base64
import os
import pytest
from typing import List, Tuple
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def test_handshake_no_compression() -> None:
    hdrs, sec_key = gen_ws_headers(compress=0)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" not in headers
    assert compress == 0

def test_handshake_with_protocols() -> None:
    protocols = "chat, superchat"
    hdrs, sec_key = gen_ws_headers(protocols=protocols)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == protocols

def test_handshake_server_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "server_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_client_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "client_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_with_extension_text() -> None:
    extension_text = "example-extension"
    hdrs, sec_key = gen_ws_headers(compress=15, extension_text=extension_text)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert extension_text in headers["Sec-Websocket-Extensions"]