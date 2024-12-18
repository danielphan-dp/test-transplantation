import base64
import os
import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from typing import List, Tuple

def gen_ws_headers(protocols: str='', compress: int=0, extension_text: str='', server_notakeover: bool=False, client_notakeover: bool=False) -> Tuple[List[Tuple[str, str]], str]:
    key = base64.b64encode(os.urandom(16)).decode()
    hdrs = [('Upgrade', 'websocket'), ('Connection', 'upgrade'), ('Sec-Websocket-Version', '13'), ('Sec-Websocket-Key', key)]
    if protocols:
        hdrs += [('Sec-Websocket-Protocol', protocols)]
    if compress:
        params = 'permessage-deflate'
        if compress < 15:
            params += '; server_max_window_bits=' + str(compress)
        if server_notakeover:
            params += '; server_no_context_takeover'
        if client_notakeover:
            params += '; client_no_context_takeover'
        if extension_text:
            params += '; ' + extension_text
        hdrs += [('Sec-Websocket-Extensions', params)]
    return (hdrs, key)

def test_handshake_no_protocol() -> None:
    hdrs, sec_key = gen_ws_headers()

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" not in headers
    assert compress == 0

def test_handshake_with_protocol() -> None:
    hdrs, sec_key = gen_ws_headers(protocols='chat')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == 'chat'

def test_handshake_with_compression() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == 'permessage-deflate; server_max_window_bits=10'
    assert compress == 10

def test_handshake_with_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == 'permessage-deflate; server_max_window_bits=10; server_no_context_takeover'
    assert compress == 10
    assert notakeover is True

def test_handshake_with_client_no_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == 'permessage-deflate; server_max_window_bits=10; client_no_context_takeover'
    assert compress == 10
    assert notakeover is False

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, extension_text='custom_extension')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == 'permessage-deflate; server_max_window_bits=10; custom_extension'
    assert compress == 10