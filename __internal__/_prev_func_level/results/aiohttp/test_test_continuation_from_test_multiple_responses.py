import pytest
import random
import struct
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.web_ws import WSMessageText
from aiohttp.http import WSCloseCode, WebSocketError

@pytest.fixture
def setup_websocket_reader(out):
    return WebSocketReader(out, 256, compress=False)

def test_build_frame_no_mask(setup_websocket_reader):
    parser = setup_websocket_reader
    data = build_frame(b"test message", WSMsgType.TEXT, use_mask=False)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res == WSMessageText(data="test message", size=12, extra="")

def test_build_frame_with_mask(setup_websocket_reader):
    parser = setup_websocket_reader
    data = build_frame(b"masked message", WSMsgType.TEXT, use_mask=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res == WSMessageText(data="masked message", size=15, extra="")

def test_build_frame_noheader(setup_websocket_reader):
    parser = setup_websocket_reader
    data = build_frame(b"no header message", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res is None  # No header should mean no message in buffer

def test_build_frame_large_message(setup_websocket_reader):
    parser = setup_websocket_reader
    large_message = b"x" * (1 << 16)  # 65536 bytes
    data = build_frame(large_message, WSMsgType.TEXT)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == large_message
    assert res.size == len(large_message)

def test_build_frame_compressed_message(setup_websocket_reader):
    parser = setup_websocket_reader
    data = build_frame(b"compressed message", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"compressed message"
    assert res.size == len(b"compressed message")

def test_build_frame_invalid_opcode(setup_websocket_reader):
    parser = setup_websocket_reader
    with pytest.raises(WebSocketError) as ctx:
        data = build_frame(b"invalid opcode", 99)  # Invalid opcode
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_build_frame_message_too_large(setup_websocket_reader):
    parser = setup_websocket_reader
    large_message = b"x" * (1 << 17)  # 131072 bytes
    data = build_frame(large_message, WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG