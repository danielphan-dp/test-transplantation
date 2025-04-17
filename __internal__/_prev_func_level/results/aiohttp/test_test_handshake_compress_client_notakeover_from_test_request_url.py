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

def test_handshake_no_compression() -> None:
    hdrs, sec_key = gen_ws_headers(compress=0)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" not in headers
    assert compress == 0

def test_handshake_with_protocol() -> None:
    hdrs, sec_key = gen_ws_headers(protocols='chat')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, protocol, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Protocol" in headers
    assert headers["Sec-Websocket-Protocol"] == 'chat'
    assert compress == 0

def test_handshake_compress_server_notakeover() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, server_notakeover=True)

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == "permessage-deflate; server_no_context_takeover"
    assert compress == 15

def test_handshake_with_extension_text() -> None:
    hdrs, sec_key = gen_ws_headers(compress=15, extension_text='custom_extension')

    req = make_mocked_request("GET", "/", headers=hdrs)

    ws = web.WebSocketResponse()
    headers, _, compress, notakeover = ws._handshake(req)

    assert "Sec-Websocket-Extensions" in headers
    assert headers["Sec-Websocket-Extensions"] == "permessage-deflate; custom_extension"
    assert compress == 15

def test_handshake_invalid_key() -> None:
    req = make_mocked_request("GET", "/", headers={"Upgrade": "websocket", "Connection": "upgrade", "Sec-Websocket-Key": "invalid_key"})

    ws = web.WebSocketResponse()
    with pytest.raises(web.HTTPBadRequest):
        ws._handshake(req)