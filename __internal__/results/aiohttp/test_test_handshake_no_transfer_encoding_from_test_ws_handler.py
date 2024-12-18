import base64
import os
import pytest
from typing import List, Tuple
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

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

def test_handshake_with_protocols() -> None:
    protocols = "chat, superchat"
    hdrs, sec_key = gen_ws_headers(protocols=protocols)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert ('Sec-Websocket-Protocol', protocols) in headers

def test_handshake_with_compression() -> None:
    compress = 10
    hdrs, sec_key = gen_ws_headers(compress=compress)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress_value, notakeover = ws._handshake(req)

    assert ('Sec-Websocket-Extensions', 'permessage-deflate; server_max_window_bits=10') in headers

def test_handshake_with_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, server_notakeover=True)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert 'server_no_context_takeover' in headers[3][1]

def test_handshake_with_client_no_context_takeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=10, client_notakeover=True)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert 'client_no_context_takeover' in headers[3][1]

def test_handshake_with_extension_text() -> None:
    extension_text = "custom_extension"
    hdrs, sec_key = gen_ws_headers(extension_text=extension_text)
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert ('Sec-Websocket-Extensions', f'permessage-deflate; {extension_text}') in headers

def test_handshake_no_transfer_encoding() -> None:
    hdrs, sec_key = gen_ws_headers()
    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Transfer-Encoding" not in headers