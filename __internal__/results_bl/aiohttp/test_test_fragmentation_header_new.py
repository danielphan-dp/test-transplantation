import asyncio
import random
import struct
import zlib
import pytest
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp._websocket.models import WS_DEFLATE_TRAILING
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader, WSMessageText

def test_build_frame_no_mask() -> None:
    data = build_frame(b"hello", WSMsgType.TEXT, use_mask=False)
    assert data[:1] == bytes([129])  # FIN + opcode for text
    assert data[1] == 5  # Length of the message

def test_build_frame_with_mask() -> None:
    data = build_frame(b"world", WSMsgType.TEXT, use_mask=True)
    assert data[:1] == bytes([129])  # FIN + opcode for text
    assert data[1] & 128 == 128  # Mask bit should be set
    assert data[2:6]  # Mask should be present

def test_build_frame_large_message() -> None:
    large_message = b"x" * 70000
    data = build_frame(large_message, WSMsgType.TEXT)
    assert data[:1] == bytes([129])  # FIN + opcode for text
    assert data[1] == 127  # Length should indicate a large message

def test_build_frame_compressed_message() -> None:
    data = build_frame(b"compressed", WSMsgType.TEXT, compress=True)
    assert data[:1] == bytes([193])  # FIN + opcode for text + compression bit
    assert len(data) < len(b"compressed")  # Compressed data should be smaller

def test_build_frame_no_header() -> None:
    data = build_frame(b"no header", WSMsgType.TEXT, noheader=True)
    assert data == b"no header"  # Should return only the message without header

def test_build_frame_empty_message() -> None:
    data = build_frame(b"", WSMsgType.TEXT)
    assert data[:1] == bytes([128])  # FIN + opcode for text
    assert data[1] == 0  # Length of the message should be 0

def test_build_frame_invalid_opcode() -> None:
    with pytest.raises(ValueError):
        build_frame(b"invalid", 10)  # Invalid opcode should raise an error

def test_build_frame_fragmented_message() -> None:
    data = build_frame(b"fragmented", WSMsgType.TEXT)
    parser = WebSocketReader()
    out = WebSocketDataQueue()
    parser._feed_data(data[:5])
    parser._feed_data(data[5:])
    res = out._buffer[0]
    assert res == WSMessageText(data="fragmented", size=10, extra="")