import base64
import os
import pytest
from typing import List, Tuple
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def test_handshake_with_protocols() -> None:
    hdrs, sec_key = gen_ws_headers(protocols='chat, superchat')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert ('Sec-Websocket-Protocol', 'chat, superchat') in headers

def test_handshake_with_compression_and_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert compress == 15
    assert 'server_no_context_takeover' in headers[3][1]

def test_handshake_with_client_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert 'client_no_context_takeover' in headers[3][1]

def test_handshake_with_empty_protocols() -> None:
    hdrs, sec_key = gen_ws_headers(protocols='')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" not in headers

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(extension_text='custom-extension')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert 'custom-extension' in headers[3][1]