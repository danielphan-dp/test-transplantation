import asyncio
import random
import struct
import zlib
import pytest
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader, WSMessageText

def test_build_frame_no_mask() -> None:
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1] == len(message)  # Payload length

def test_build_frame_with_mask() -> None:
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1] & 0x80 == 0x80  # Mask bit set

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1] == 126  # Payload length indicator for 16-bit length
    assert struct.unpack('>H', frame[2:4])[0] == len(message)  # Actual length

def test_build_frame_compressed_message() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame[:1] == bytes([193])  # FIN + opcode + compress bit
    assert len(frame) < len(message) + 2  # Compressed frame should be smaller

def test_build_frame_noheader() -> None:
    message = b"no header"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message  # Should return only the message without header

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([128])  # FIN + opcode
    assert frame[1] == 0  # Payload length should be 0

def test_build_frame_invalid_opcode() -> None:
    message = b"test"
    opcode = 10  # Invalid opcode
    with pytest.raises(ValueError):
        build_frame(message, opcode)