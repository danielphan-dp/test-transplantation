import pytest
import struct
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.http import WebSocketError, WSCloseCode

def test_build_frame_no_mask() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, use_mask=False)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1:2] == struct.pack("!B", len(message))  # Length

def test_build_frame_with_mask() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, use_mask=True)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1:2] == struct.pack("!B", len(message) | 0b10000000)  # Length with mask bit

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1:3] == struct.pack("!B", 126)  # Length indicator for 65536
    assert data[3:5] == struct.pack("!H", len(message))  # Actual length

def test_build_frame_compressed_message() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, compress=True)
    assert data[:1] == struct.pack("!B", 0b11000001)  # FIN + opcode + compress bit
    assert data[1:2] == struct.pack("!B", len(message))  # Length

def test_build_frame_noheader() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, noheader=True)
    assert data == bytearray(message)  # No header should return just the message

def test_build_frame_invalid_opcode() -> None:
    message = b"hello"
    opcode = 0xFF  # Invalid opcode
    with pytest.raises(ValueError):
        build_frame(message, opcode)