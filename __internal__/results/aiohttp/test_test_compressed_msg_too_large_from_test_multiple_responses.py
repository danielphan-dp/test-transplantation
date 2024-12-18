import pytest
import struct
from aiohttp._websocket.reader import WebSocketReader
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.helpers import build_frame

def test_msg_too_large_with_mask(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 256, WSMsgType.TEXT, use_mask=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_compressed_msg_with_noheader(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"aaa" * 256, WSMsgType.TEXT, compress=True, noheader=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_msg_too_large_not_fin_with_mask(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 256, WSMsgType.TEXT, is_fin=False, use_mask=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_large_compressed_msg_with_fin(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"aaa" * 256, WSMsgType.TEXT, compress=True, is_fin=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_empty_message(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"", WSMsgType.TEXT)
    parser._feed_data(data)  # Should not raise an error
    assert parser._frame_payload_len == 0  # Ensure no payload is stored

def test_large_message_with_fin(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=False)
    data = build_frame(b"text" * 256, WSMsgType.TEXT, is_fin=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG