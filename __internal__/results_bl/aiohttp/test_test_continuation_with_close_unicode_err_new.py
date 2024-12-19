import pytest
from unittest import mock
from aiohttp.http import WSCloseCode, WSMsgType, WebSocketError
from aiohttp._websocket.helpers import build_close_frame

def test_build_close_frame_valid_code():
    frame = build_close_frame(1000, b'')
    assert frame == b'\x03\xe8'  # Example expected output, adjust as necessary

def test_build_close_frame_with_message():
    frame = build_close_frame(1000, b'Close message')
    assert frame.endswith(b'Close message')

def test_build_close_frame_noheader():
    frame = build_close_frame(1000, b'', noheader=True)
    assert frame.startswith(b'\x03\xe8')

def test_build_close_frame_invalid_code():
    with pytest.raises(ValueError):
        build_close_frame(9999)  # Assuming 9999 is an invalid close code

def test_build_close_frame_empty_message():
    frame = build_close_frame(1000, b'')
    assert frame == build_close_frame(1000)  # Should be the same as default

def test_build_close_frame_unicode_message():
    frame = build_close_frame(1000, b'\xf4\x90\x80\x80')
    assert frame.endswith(b'\xf4\x90\x80\x80')  # Check if the unicode message is included

def test_build_close_frame_edge_case_zero_code():
    frame = build_close_frame(0, b'')
    assert frame == b'\x00\x00'  # Example expected output for code 0, adjust as necessary

def test_build_close_frame_edge_case_max_code():
    frame = build_close_frame(65535, b'')
    assert frame == b'\xff\xff'  # Example expected output for max code, adjust as necessary