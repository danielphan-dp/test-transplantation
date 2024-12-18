import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.web_ws import WebSocketDataQueue

def test_build_frame_no_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame.startswith(bytes([128 | opcode]))  # FIN + opcode
    assert frame[1] == len(message)  # Payload length

def test_build_frame_with_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame.startswith(bytes([128 | opcode | 128]))  # FIN + opcode + mask bit
    assert frame[1] == len(message)  # Payload length

def test_build_frame_noheader() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message  # No header should return just the message

def test_build_frame_compressed() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(bytes([128 | opcode | 64]))  # FIN + opcode + compress bit

def test_build_frame_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame.startswith(bytes([128 | opcode]))  # FIN + opcode
    assert frame[1] == 126  # Payload length should indicate extended length
    assert frame[2:4] == (len(message)).to_bytes(2, 'big')  # Extended length

def test_build_frame_too_large_message() -> None:
    message = b"A" * (1 << 17)  # 131072 bytes
    opcode = WSMsgType.TEXT
    with pytest.raises(ValueError):
        build_frame(message, opcode)  # Should raise an error for too large message

def test_build_frame_fin_flag() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, is_fin=False)
    assert not (frame[0] & 0x80)  # FIN flag should be 0

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame.startswith(bytes([128 | opcode]))  # FIN + opcode
    assert frame[1] == 0  # Payload length should be 0

def test_build_frame_noheader_with_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True, noheader=True)
    assert frame == bytearray(message)  # No header should return just the masked message

def test_build_frame_compressed_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(bytes([128 | opcode | 64]))  # FIN + opcode + compress bit
    assert frame[1] == 126  # Payload length should indicate extended length
    assert frame[2:4] == (len(message)).to_bytes(2, 'big')  # Extended length