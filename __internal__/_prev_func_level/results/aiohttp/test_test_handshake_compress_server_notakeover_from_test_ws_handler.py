import base64
import os
import pytest
from typing import List, Tuple
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def test_handshake_no_protocol() -> None:
    hdrs, sec_key = gen_ws_headers()

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert compress == 0
    assert notakeover is False
    assert "Sec-Websocket-Extensions" not in headers

def test_handshake_with_protocol() -> None:
    hdrs, sec_key = gen_ws_headers(protocols="chat")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == "chat"

def test_handshake_compress_client_notakeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert compress == 10
    assert notakeover is True
    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == (
        "permessage-deflate; client_no_context_takeover"
    )

def test_handshake_invalid_compress_value() -> None:
    hdrs, sec_key = gen_ws_headers(compress=20)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert compress == 0
    assert notakeover is False
    assert "Sec-Websocket-Extensions" not in headers

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, extension_text="custom_extension")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == (
        "permessage-deflate; server_max_window_bits=15; custom_extension"
    )