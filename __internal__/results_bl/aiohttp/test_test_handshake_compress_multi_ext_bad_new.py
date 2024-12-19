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

def test_handshake_with_protocols() -> None:
    hdrs, sec_key = gen_ws_headers(protocols="chat, superchat")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == "chat, superchat"

def test_handshake_with_server_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "server_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_with_client_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "client_no_context_takeover" in headers["Sec-Websocket-Extensions"]

def test_handshake_with_multiple_extensions() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, extension_text="ext1, ext2")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "ext1" in headers["Sec-Websocket-Extensions"]
    assert "ext2" in headers["Sec-Websocket-Extensions"]