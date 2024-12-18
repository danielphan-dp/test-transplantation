import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WSMsgType, WSCloseCode
from aiohttp.http_websocket import WSMessageClose

def test_build_close_frame_default() -> None:
    frame = build_close_frame()
    assert frame == build_close_frame(1000, b'', False)

def test_build_close_frame_with_code() -> None:
    frame = build_close_frame(1001)
    assert frame == build_close_frame(1001, b'', False)

def test_build_close_frame_with_message() -> None:
    frame = build_close_frame(1002, b"test")
    assert frame == build_close_frame(1002, b"test", False)

def test_build_close_frame_noheader() -> None:
    frame = build_close_frame(1003, b"test", noheader=True)
    assert frame == build_close_frame(1003, b"test", noheader=True)

def test_build_close_frame_invalid_code() -> None:
    with pytest.raises(ValueError):
        build_close_frame(3000)

def test_build_close_frame_empty_message() -> None:
    frame = build_close_frame(1000, b'')
    assert frame == build_close_frame(1000, b'', False)

def test_build_close_frame_large_message() -> None:
    large_message = b'a' * 1000
    frame = build_close_frame(1000, large_message)
    assert frame == build_close_frame(1000, large_message, False)