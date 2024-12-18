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
    assert data[1] == len(message)  # Payload length

def test_build_frame_with_mask() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, use_mask=True)
    assert data[:1] == struct.pack("!B", 0b10000001 | 0b10000000)  # FIN + opcode + mask bit
    assert data[1] == len(message)  # Payload length
    mask = data[2:6]
    assert len(mask) == 4  # Mask should be 4 bytes

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1] == 126  # Payload length indicator for large message
    assert data[2:4] == struct.pack("!H", len(message))  # Actual length follows

def test_build_frame_compressed_message() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, compress=True)
    assert data[:1] == struct.pack("!B", 0b10000001 | 0b01000000)  # FIN + opcode + compress bit
    assert len(data) > len(message)  # Compressed data should be larger

def test_build_frame_noheader() -> None:
    message = b"hello"
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode, noheader=True)
    assert data == bytearray(message)  # Should return only the message without header

def test_build_frame_invalid_opcode() -> None:
    message = b"hello"
    with pytest.raises(ValueError):
        build_frame(message, 99)  # Invalid opcode should raise an error

def test_build_frame_message_too_large() -> None:
    message = b"x" * (1 << 20)  # 1048576 bytes
    opcode = WSMsgType.TEXT
    with pytest.raises(WebSocketError) as ctx:
        build_frame(message, opcode)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG  # Should raise message too big error

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    data = build_frame(message, opcode)
    assert data[:1] == struct.pack("!B", 0b10000001)  # FIN + opcode
    assert data[1] == 0  # Payload length should be 0