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

    assert compress == 0
    assert notakeover is False
    assert "Sec-Websocket-Extensions" not in headers

def test_handshake_with_protocols() -> None:
    hdrs, sec_key = gen_ws_headers(protocols='chat, superchat')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == 'chat, superchat'

def test_handshake_client_notakeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert compress == 15
    assert notakeover is True
    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == (
        "permessage-deflate; client_no_context_takeover"
    )

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, extension_text='foo=bar')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert compress == 15
    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == (
        "permessage-deflate; foo=bar"
    )