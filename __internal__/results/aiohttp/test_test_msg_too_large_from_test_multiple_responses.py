import pytest
import struct
from aiohttp._websocket.reader import WebSocketReader
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.helpers import build_frame

def test_msg_too_large_not_fin(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 256, WSMsgType.TEXT, is_fin=False)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_compressed_msg_too_large(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"aaa" * 256, WSMsgType.TEXT, compress=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_msg_with_mask(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"hello", WSMsgType.TEXT, use_mask=True)
    parser._feed_data(data)
    assert parser._frame_opcode == WSMsgType.TEXT

def test_msg_no_header(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"hello", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    assert parser._frame_opcode == WSMsgType.TEXT

def test_large_message_with_header(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"x" * (1 << 16), WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_empty_message(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"", WSMsgType.TEXT)
    parser._feed_data(data)
    assert parser._frame_opcode == WSMsgType.TEXT

def test_message_with_compression(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"compressed message", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    assert parser._frame_opcode == WSMsgType.TEXT

def test_message_with_invalid_opcode(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = struct.pack("!BB", 0b00000001, 0b00000001) + b"invalid"
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR