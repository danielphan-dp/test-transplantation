import pytest
import random
import zlib
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.reader import WebSocketDataQueue
from aiohttp.http_websocket import WebSocketReader
from aiohttp._websocket.helpers import build_frame

def test_build_frame_no_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1:2] == bytes([5])    # Length of the message

def test_build_frame_with_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1:2] == bytes([5 | 128])  # Length of the message with mask bit set

def test_build_frame_noheader() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message  # Should return only the message without header

def test_build_frame_compressed() -> None:
    message = b"Hello" * 100
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame[:1] == bytes([193])  # FIN + opcode + compress bit
    assert len(frame) < len(message)  # Compressed frame should be smaller

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([129])  # FIN + opcode
    assert frame[1:3] == bytes([126, 255, 255])  # Length field for 65536 bytes

def test_build_frame_exceeding_max_length() -> None:
    message = b"x" * (1 << 17)  # 131072 bytes
    opcode = WSMsgType.TEXT
    with pytest.raises(WebSocketError) as ctx:
        build_frame(message, opcode)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_build_frame_fin_false() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, is_fin=False)
    assert frame[:1] == bytes([1])  # FIN bit should be 0

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:1] == bytes([128])  # FIN + opcode
    assert frame[1:2] == bytes([0])    # Length of the message is 0