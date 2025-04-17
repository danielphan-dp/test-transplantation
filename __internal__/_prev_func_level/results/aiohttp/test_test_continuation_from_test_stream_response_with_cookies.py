import pytest
import struct
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.web_ws import WebSocketDataQueue

def test_build_frame_no_mask() -> None:
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=False)
    expected_header = PACK_LEN1(128 | opcode, len(message))
    assert frame.startswith(expected_header)
    assert frame[1:] == message

def test_build_frame_with_mask() -> None:
    message = b"test"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    expected_header = PACK_LEN1(128 | opcode | 128, len(message))
    assert frame.startswith(expected_header)
    assert frame[5:] == bytearray(message)  # Check masked message

def test_build_frame_large_message() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    expected_header = PACK_LEN2(128 | opcode, 126, len(message))
    assert frame.startswith(expected_header)

def test_build_frame_noheader() -> None:
    message = b"noheader"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, noheader=True)
    assert frame == message

def test_build_frame_compressed() -> None:
    message = b"compressed"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, compress=True)
    assert frame.startswith(PACK_LEN1(128 | opcode | 64, len(frame) - 2))  # Check for compression header

def test_build_frame_invalid_opcode() -> None:
    message = b"test"
    with pytest.raises(ValueError):
        build_frame(message, 10)  # Invalid opcode

def test_build_frame_empty_message() -> None:
    message = b""
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode)
    expected_header = PACK_LEN1(128 | opcode, 0)
    assert frame.startswith(expected_header)
    assert frame[1:] == message

def test_build_frame_fin_false() -> None:
    message = b"line1"
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, is_fin=False)
    expected_header = PACK_LEN1(opcode, len(message))
    assert frame.startswith(expected_header)  # Check FIN bit is not set
    assert frame[1:] == message

def test_build_frame_large_message_with_mask() -> None:
    message = b"x" * (1 << 16)  # 65536 bytes
    opcode = WSMsgType.TEXT
    frame = build_frame(message, opcode, use_mask=True)
    expected_header = PACK_LEN2(128 | opcode | 128, 126, len(message))
    assert frame.startswith(expected_header)