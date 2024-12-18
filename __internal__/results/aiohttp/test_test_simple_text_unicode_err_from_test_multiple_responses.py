import pytest
import struct
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.helpers import build_frame

def test_build_frame_no_mask() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame.startswith(struct.pack("!B", 0b10000001))  # FIN + opcode
    assert frame[1] == len(message)  # Payload length

def test_build_frame_with_mask() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame.startswith(struct.pack("!B", 0b10000001))  # FIN + opcode
    assert frame[1] == len(message)  # Payload length
    assert len(frame) > len(message) + 6  # Header + mask

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame.startswith(struct.pack("!B", 0b10000001))  # FIN + opcode
    assert frame[1] == 126  # Payload length indicator for 65536 bytes
    assert frame[2:4] == struct.pack("!H", len(message))  # Actual length

def test_build_frame_compressed_message() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(struct.pack("!B", 0b11000001))  # FIN + opcode + compress flag
    assert len(frame) > len(message)  # Compressed frame should be larger

def test_build_frame_invalid_unicode() -> None:
    message = b"\xf4\x90\x80\x80"  # Invalid UTF-8 sequence
    opcode = WSMsgType.TEXT
    with pytest.raises(WebSocketError) as ctx:
        build_frame(message, opcode)
    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_build_frame_noheader() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message  # Should return only the message without header

def test_build_frame_fin_false() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, is_fin=False)
    assert not (frame[0] & 0b10000000)  # FIN bit should be 0

def test_build_frame_message_too_large() -> None:
    message = b"x" * (1 << 20)  # 1048576 bytes
    opcode = WSMsgType.TEXT
    with pytest.raises(WebSocketError) as ctx:
        build_frame(message, opcode)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG