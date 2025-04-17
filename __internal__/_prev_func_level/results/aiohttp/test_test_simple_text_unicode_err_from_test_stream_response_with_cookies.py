import pytest
import struct
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.helpers import build_frame

def test_build_frame_with_mask_and_noheader() -> None:
    message = b"Hello, World!"
    opcode = WSMsgType.TEXT
    use_mask = True
    noheader = True
    result = build_frame(message, opcode, use_mask=use_mask, noheader=noheader)
    assert isinstance(result, bytearray)
    assert result == bytearray(message)

def test_build_frame_with_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    result = build_frame(message, opcode)
    assert len(result) > 0
    assert result[0] & 0x0F == opcode
    assert result[1] & 0x7F == 127

def test_build_frame_with_compression() -> None:
    message = b"Compressed message"
    opcode = WSMsgType.TEXT
    compress = True
    result = build_frame(message, opcode, compress=compress)
    assert len(result) < len(message)  # Compressed message should be smaller

def test_build_frame_invalid_opcode() -> None:
    message = b"Invalid opcode"
    opcode = 0xFF  # Invalid opcode
    with pytest.raises(ValueError):
        build_frame(message, opcode)

def test_build_frame_with_fin_false() -> None:
    message = b"Not final frame"
    opcode = WSMsgType.TEXT
    is_fin = False
    result = build_frame(message, opcode, is_fin=is_fin)
    assert result[0] & 0x80 == 0  # FIN bit should be 0

def test_build_frame_with_mask() -> None:
    message = b"Masked message"
    opcode = WSMsgType.TEXT
    use_mask = True
    result = build_frame(message, opcode, use_mask=use_mask)
    assert len(result) > len(message)  # Masking adds extra bytes

def test_build_frame_noheader() -> None:
    message = b"No header message"
    opcode = WSMsgType.TEXT
    noheader = True
    result = build_frame(message, opcode, noheader=noheader)
    assert result == bytearray(message)  # Should return only the message

def test_build_frame_with_invalid_message_type() -> None:
    message = 12345  # Invalid message type
    opcode = WSMsgType.TEXT
    with pytest.raises(TypeError):
        build_frame(message, opcode)