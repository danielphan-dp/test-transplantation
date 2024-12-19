import base64
import os
from typing import List, Tuple
import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def test_handshake_no_protocols() -> None:
    hdrs, sec_key = gen_ws_headers()

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" not in headers

def test_handshake_with_protocols() -> None:
    hdrs, sec_key = gen_ws_headers(protocols="chat, superchat")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert ("Sec-Websocket-Protocol", "chat, superchat") in headers

def test_handshake_compress_with_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "server_no_context_takeover" in headers[3][1]

def test_handshake_compress_with_client_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "client_no_context_takeover" in headers[3][1]

def test_handshake_empty_key() -> None:
    hdrs, sec_key = gen_ws_headers()

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert sec_key is not None
    assert len(sec_key) > 0

def test_handshake_invalid_compress_value() -> None:
    hdrs, sec_key = gen_ws_headers(compress=20)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" not in headers
    assert compress == 0