import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketDataQueue, WSMessageText, WSMessagePing, WebSocketError, WSCloseCode

def test_build_frame_no_mask(out: WebSocketDataQueue) -> None:
    data = build_frame(b"test", WSMsgType.TEXT, use_mask=False)
    out._feed_data(data)
    res = out._buffer[0]
    assert res == WSMessageText(data="test", size=4, extra="")

def test_build_frame_with_mask(out: WebSocketDataQueue) -> None:
    data = build_frame(b"test", WSMsgType.TEXT, use_mask=True)
    out._feed_data(data)
    res = out._buffer[0]
    assert res == WSMessageText(data="test", size=4, extra="")

def test_build_frame_noheader(out: WebSocketDataQueue) -> None:
    data = build_frame(b"test", WSMsgType.TEXT, noheader=True)
    out._feed_data(data)
    assert out._buffer == []

def test_build_frame_large_message(out: WebSocketDataQueue) -> None:
    data = build_frame(b"x" * (1 << 16), WSMsgType.TEXT)
    out._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"x" * (1 << 16)

def test_build_frame_compressed_message(out: WebSocketDataQueue) -> None:
    data = build_frame(b"compressed", WSMsgType.TEXT, compress=True)
    out._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"compressed"

def test_build_frame_invalid_opcode(out: WebSocketDataQueue) -> None:
    with pytest.raises(WebSocketError) as ctx:
        build_frame(b"test", 99)  # Invalid opcode
    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_build_frame_empty_message(out: WebSocketDataQueue) -> None:
    data = build_frame(b"", WSMsgType.TEXT)
    out._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"" and res.size == 0

def test_build_frame_fin_false(out: WebSocketDataQueue) -> None:
    data = build_frame(b"test", WSMsgType.TEXT, is_fin=False)
    out._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"test" and res.size == 4

def test_build_frame_message_too_large(out: WebSocketDataQueue) -> None:
    data = build_frame(b"x" * (1 << 17), WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        out._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG