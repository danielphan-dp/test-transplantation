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
    hdrs, sec_key = gen_ws_headers(protocols='chat, superchat')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == 'chat, superchat'

def test_handshake_with_server_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=9, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "server_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_with_client_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=9, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "client_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(compress=9, extension_text='custom-extension')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == (
        "permessage-deflate; server_max_window_bits=9; custom-extension"
    )