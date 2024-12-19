import pytest
import random
import zlib
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp._websocket.helpers import build_frame

def test_build_frame_no_mask() -> None:
    message = b"Hello, World!"
    frame = build_frame(message, WSMsgType.TEXT, use_mask=False)
    assert frame.startswith(bytes([129]))  # FIN + opcode for text

def test_build_frame_with_mask() -> None:
    message = b"Hello, World!"
    frame = build_frame(message, WSMsgType.TEXT, use_mask=True)
    assert frame[0] & 0b10000000 == 128  # FIN bit set
    assert frame[1] & 0b10000000 == 128  # Mask bit set

def test_build_frame_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    frame = build_frame(message, WSMsgType.TEXT)
    assert len(frame) > 0  # Ensure frame is created

def test_build_frame_compressed_message() -> None:
    message = b"Hello, World!"
    frame = build_frame(message, WSMsgType.TEXT, compress=True)
    assert frame.startswith(bytes([192]))  # FIN + opcode + compress bit

def test_build_frame_noheader() -> None:
    message = b"Hello, World!"
    frame = build_frame(message, WSMsgType.TEXT, noheader=True)
    assert frame == bytearray(message)  # No header should return raw message

def test_build_frame_invalid_unicode() -> None:
    parser = WebSocketReader()
    data = build_frame(b"\xf4\x90\x80\x80", WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_build_frame_empty_message() -> None:
    frame = build_frame(b"", WSMsgType.TEXT)
    assert len(frame) > 0  # Ensure frame is created for empty message

def test_build_frame_message_length_126() -> None:
    message = b"A" * 126
    frame = build_frame(message, WSMsgType.TEXT)
    assert frame[1] == 126  # Length should be encoded as 126

def test_build_frame_message_length_127() -> None:
    message = b"A" * (1 << 17)  # 131072 bytes
    frame = build_frame(message, WSMsgType.TEXT)
    assert frame[1] == 127  # Length should be encoded as 127