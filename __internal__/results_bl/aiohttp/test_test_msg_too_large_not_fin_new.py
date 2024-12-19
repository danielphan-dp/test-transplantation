import pytest
import random
import zlib
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp.http_websocket import WebSocketReader

def test_msg_too_large_fin(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 256, WSMsgType.TEXT, is_fin=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_msg_with_mask(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"masked text", WSMsgType.TEXT, use_mask=True)
    parser._feed_data(data)
    assert parser._buffer == b"masked text"

def test_msg_no_header(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"no header", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    assert parser._buffer == b"no header"

def test_large_msg_with_mask(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 300, WSMsgType.TEXT, use_mask=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_compressed_message(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"compressed text", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    assert parser._buffer == b"compressed text"