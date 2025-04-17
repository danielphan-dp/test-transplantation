import base64
import os
import pytest
from typing import List, Tuple
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def test_handshake_with_protocols() -> None:
    protocols = "chat, superchat"
    hdrs, sec_key = gen_ws_headers(protocols=protocols)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == protocols, hdrs

def test_handshake_with_compression_and_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert "permessage-deflate; server_max_window_bits=10; server_no_context_takeover" in headers["Sec-Websocket-Extensions"], hdrs
    assert compress == 10

def test_handshake_with_extension_text() -> None:
    extension_text = "custom-extension"
    hdrs, sec_key = gen_ws_headers(extension_text=extension_text)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == extension_text, hdrs

def test_handshake_without_compression() -> None:
    hdrs, sec_key = gen_ws_headers(compress=0)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" not in headers
    assert compress == 0

def test_handshake_with_invalid_protocol() -> None:
    hdrs, sec_key = gen_ws_headers(protocols="")

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" not in headers

def test_handshake_with_client_notakeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == "permessage-deflate; client_no_context_takeover", hdrs
    assert compress == 15