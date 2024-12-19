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

    assert ('Sec-Websocket-Protocol', protocols) in headers

def test_handshake_with_compression() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert ('Sec-Websocket-Extensions', 'permessage-deflate; server_max_window_bits=10') in headers

def test_handshake_with_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert 'server_no_context_takeover' in headers['Sec-Websocket-Extensions']

def test_handshake_with_client_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert 'client_no_context_takeover' in headers['Sec-Websocket-Extensions']

def test_handshake_with_extension_text() -> None:
    extension_text = "custom-extension"
    hdrs, sec_key = gen_ws_headers(extension_text=extension_text)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert extension_text in headers['Sec-Websocket-Extensions']