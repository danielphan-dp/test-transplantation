import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WSCloseCode, WebSocketError

def test_build_close_frame_valid_code() -> None:
    frame = build_close_frame(1000, b'Normal Closure', noheader=False)
    assert frame.startswith(b'\x88')  # Check for correct opcode
    assert frame[1:3] == b'\x03\xe8'  # Check for close code 1000

def test_build_close_frame_invalid_code() -> None:
    with pytest.raises(ValueError):
        build_close_frame(9999, b'Invalid Code', noheader=False)

def test_build_close_frame_empty_message() -> None:
    frame = build_close_frame(1000, b'', noheader=False)
    assert frame.startswith(b'\x88')
    assert frame[1:3] == b'\x03\xe8'
    assert len(frame) == 4  # Only close code, no message

def test_build_close_frame_noheader() -> None:
    frame = build_close_frame(1000, b'Normal Closure', noheader=True)
    assert frame.startswith(b'\x88')
    assert frame[1:3] == b'\x03\xe8'
    assert b'Normal Closure' in frame

def test_build_close_frame_unicode_message() -> None:
    frame = build_close_frame(1000, b'\xf4\x90\x80\x80', noheader=False)
    assert frame.startswith(b'\x88')
    assert frame[1:3] == b'\x03\xe8'
    assert b'\xf4\x90\x80\x80' in frame

def test_build_close_frame_large_message() -> None:
    large_message = b'a' * 1234  # Exceeding typical message size
    frame = build_close_frame(1000, large_message, noheader=False)
    assert frame.startswith(b'\x88')
    assert frame[1:3] == b'\x03\xe8'
    assert large_message in frame