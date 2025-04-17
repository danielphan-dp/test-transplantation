import pytest
import struct
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.web_exceptions import WebSocketError
from aiohttp.http_websocket import WSMessageText

def test_build_frame_no_mask(out: WebSocketDataQueue) -> None:
    data = build_frame(b"test message", WSMsgType.TEXT, use_mask=False)
    parser = WebSocketReader(out, 0, compress=False)
    parser._feed_data(data)
    
    res = out._buffer[0]
    assert res == WSMessageText(data="test message", size=12, extra="")

def test_build_frame_with_mask(out: WebSocketDataQueue) -> None:
    data = build_frame(b"masked message", WSMsgType.TEXT, use_mask=True)
    parser = WebSocketReader(out, 0, compress=False)
    parser._feed_data(data)
    
    res = out._buffer[0]
    assert res == WSMessageText(data="masked message", size=14, extra="")

def test_build_frame_noheader(out: WebSocketDataQueue) -> None:
    data = build_frame(b"no header", WSMsgType.TEXT, noheader=True)
    parser = WebSocketReader(out, 0, compress=False)
    parser._feed_data(data)
    
    assert out._buffer == []

def test_build_frame_large_message(out: WebSocketDataQueue) -> None:
    large_message = b"x" * (1 << 16)  # 65536 bytes
    data = build_frame(large_message, WSMsgType.TEXT)
    parser = WebSocketReader(out, 0, compress=False)
    parser._feed_data(data)
    
    res = out._buffer[0]
    assert res.data == large_message
    assert res.size == len(large_message)

def test_build_frame_compressed_message(out: WebSocketDataQueue) -> None:
    data = build_frame(b"compressed message", WSMsgType.TEXT, compress=True)
    parser = WebSocketReader(out, 0, compress=True)
    parser._feed_data(data)
    
    res = out._buffer[0]
    assert res.data == b"compressed message"
    assert res.size == len(b"compressed message")