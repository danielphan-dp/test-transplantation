import pytest
import struct
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.http import WebSocketError, WSCloseCode

@pytest.fixture
def out():
    return WebSocketDataQueue()

@pytest.fixture
def parser(out):
    return WebSocketReader(out, 256, compress=False)

def test_build_frame_no_mask(out):
    data = build_frame(b"test", WSMsgType.TEXT, use_mask=False)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1] == 4  # Length of the message

def test_build_frame_with_mask(out):
    data = build_frame(b"test", WSMsgType.TEXT, use_mask=True)
    assert data[:1] == struct.pack("!B", 0b10000001 | 0b10000000)  # FIN + opcode + mask bit
    assert data[1] == 4  # Length of the message

def test_build_frame_noheader(out):
    data = build_frame(b"test", WSMsgType.TEXT, noheader=True)
    assert data == b'test'  # No header should return just the message

def test_build_frame_large_message(out):
    data = build_frame(b"x" * (1 << 16), WSMsgType.TEXT)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1] == 126  # Length indicator for large message

def test_build_frame_compressed_message(out):
    data = build_frame(b"hello", WSMsgType.TEXT, compress=True)
    assert data[:1] == struct.pack("!B", 0b10000001 | 0b01000000)  # FIN + opcode + compress bit

def test_build_frame_invalid_opcode(out):
    with pytest.raises(ValueError):
        build_frame(b"test", 10)  # Invalid opcode

def test_build_frame_message_too_large(parser):
    data = build_frame(b"text" * 256, WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_build_frame_not_fin(parser):
    data = build_frame(b"text" * 256, WSMsgType.TEXT, is_fin=False)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_build_frame_compressed_msg_too_large(parser):
    data = build_frame(b"aaa" * 256, WSMsgType.TEXT, compress=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG