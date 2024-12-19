import pytest
import random
import zlib
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp.http_websocket import WebSocketReader

def test_build_frame_no_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    assert frame[:2] == PACK_LEN1(128 | opcode, len(message))

def test_build_frame_with_mask() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    assert frame[0] & 128 == 128  # Check if mask bit is set

def test_build_frame_large_message() -> None:
    message = b"A" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:2] == PACK_LEN2(128 | opcode, 126, len(message))

def test_build_frame_noheader() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message

def test_build_frame_compressed_message() -> None:
    message = b"Hello" * 1000
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame[:2] & 64 == 64  # Check if compressed bit is set

def test_build_frame_compressed_message_too_large(out: WebSocketDataQueue) -> None:
    parser = WebSocketReader(out, 256, compress=True)
    data = build_frame(b"aaa" * 256, WSMsgType.TEXT, compress=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_build_frame_fin_flag() -> None:
    message = b"Hello"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, is_fin=False)
    assert frame[0] & 128 == 0  # Check if FIN bit is not set

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    assert frame[:2] == PACK_LEN1(128 | opcode, 0)  # Check for empty message handling