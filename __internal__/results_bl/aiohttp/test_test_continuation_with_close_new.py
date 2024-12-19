import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http.WSMsgType import CLOSE
from aiohttp.http_websocket import WSMessageClose

def test_build_close_frame_default():
    result = build_close_frame()
    expected = build_close_frame(1000, b'', noheader=False)
    assert result == expected

def test_build_close_frame_with_code():
    result = build_close_frame(1001)
    expected = build_close_frame(1001, b'', noheader=False)
    assert result == expected

def test_build_close_frame_with_message():
    result = build_close_frame(1002, b"test")
    expected = build_close_frame(1002, b"test", noheader=False)
    assert result == expected

def test_build_close_frame_noheader():
    result = build_close_frame(1003, b"test", noheader=True)
    expected = build_close_frame(1003, b"test", noheader=True)
    assert result == expected

def test_build_close_frame_invalid_code():
    with pytest.raises(ValueError):
        build_close_frame(9999)

def test_build_close_frame_empty_message():
    result = build_close_frame(1004, b'')
    expected = build_close_frame(1004, b'', noheader=False)
    assert result == expected

def test_build_close_frame_large_message():
    large_message = b'a' * 1000
    result = build_close_frame(1005, large_message)
    expected = build_close_frame(1005, large_message, noheader=False)
    assert result == expected