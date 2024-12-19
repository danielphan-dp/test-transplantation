import asyncio
import random
import struct
import zlib
from unittest import mock
import pytest
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WSMessageText, WSMessagePing, WebSocketReader, WebSocketDataQueue

def test_build_frame_no_mask():
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame[:1] == bytes([128 | opcode])  # FIN + opcode
    assert frame[1:2] == bytes([4])  # Length of the message
    assert frame[2:] == message  # Payload should match

def test_build_frame_with_mask():
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert len(frame) == 10  # Header + mask + payload
    assert frame[0] == (128 | opcode)  # FIN + opcode
    assert frame[1] & 0x80 == 0x80  # Mask bit should be set
    assert frame[2:] != message  # Payload should be masked

def test_build_frame_large_message():
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([128 | opcode | 0x00])  # FIN + opcode
    assert frame[1:3] == bytes([126, 0])  # Length should be 126
    assert frame[3:] == message  # Payload should match

def test_build_frame_compressed_message():
    message = b"compressed data"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame[:1] == bytes([128 | opcode | 0x40])  # FIN + opcode + compress bit
    assert frame[1] == 14  # Length of the compressed message

def test_build_frame_noheader():
    message = b"noheader"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message  # Should return only the message without header

def test_build_frame_empty_message():
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([128 | opcode])  # FIN + opcode
    assert frame[1:2] == bytes([0])  # Length of the message
    assert frame[2:] == message  # Payload should match

def test_build_frame_invalid_opcode():
    message = b"test"
    with pytest.raises(ValueError):
        build_frame(message, 10)  # Invalid opcode, should raise an error