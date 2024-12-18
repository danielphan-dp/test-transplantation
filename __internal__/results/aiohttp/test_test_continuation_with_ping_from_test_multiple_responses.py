import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketDataQueue, WSMessageText, WSMessagePing, WebSocketError, WSCloseCode

def test_build_frame_no_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame.startswith(bytes([0b10000000 | opcode]))  # FIN + opcode
    assert frame[1] == len(message)  # Payload length

def test_build_frame_with_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame.startswith(bytes([0b10000000 | opcode | 0b10000000]))  # FIN + opcode + mask bit
    assert frame[1] == len(message)  # Payload length

def test_build_frame_compressed() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(bytes([0b10000000 | opcode | 0b01000000]))  # FIN + opcode + compress bit

def test_build_frame_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame.startswith(bytes([0b10000000 | opcode]))  # FIN + opcode
    assert frame[1] == 126  # Payload length indicator for large message
    assert frame[2:4] == (len(message)).to_bytes(2, 'big')  # Actual length

def test_build_frame_noheader() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == bytearray(message)  # No header should return just the message

def test_build_frame_invalid_opcode() -> None:
    message = b"Hello"
    with pytest.raises(ValueError):
        build_frame(message, 99)  # Invalid opcode

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame.startswith(bytes([0b10000000 | opcode]))  # FIN + opcode
    assert frame[1] == 0  # Payload length for empty message

def test_build_frame_with_noheader_and_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True, noheader=True)
    assert frame == bytearray(message)  # No header should return just the message even with mask

def test_build_frame_compressed_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(bytes([0b10000000 | opcode | 0b01000000]))  # FIN + opcode + compress bit
    assert frame[1] == 126  # Payload length indicator for large message
    assert frame[2:4] == (len(message)).to_bytes(2, 'big')  # Actual length

def test_build_frame_message_too_large() -> None:
    message = b"A" * (1 << 20)  # 1048576 bytes
    opcode = WSMsgType.TEXT
    with pytest.raises(WebSocketError) as ctx:
        build_frame(message, opcode)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG  # Expecting message too big error