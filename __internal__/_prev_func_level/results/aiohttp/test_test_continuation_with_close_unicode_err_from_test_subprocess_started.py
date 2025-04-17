import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WSCloseCode, WebSocketError
from aiohttp.http import WSMsgType
from aiohttp._websocket.reader import WebSocketReader
from aiohttp._websocket import WebSocketDataQueue

def test_build_close_frame_valid() -> None:
    frame = build_close_frame(1000, b'Normal Closure', noheader=False)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_invalid_code() -> None:
    with pytest.raises(ValueError):
        build_close_frame(9999, b'Invalid Code', noheader=False)

def test_build_close_frame_empty_message() -> None:
    frame = build_close_frame(1000, b'', noheader=False)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_noheader() -> None:
    frame = build_close_frame(1000, b'Normal Closure', noheader=True)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_unicode_message() -> None:
    frame = build_close_frame(1000, b'\xf4\x90\x80\x80', noheader=False)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_invalid_unicode_message() -> None:
    with pytest.raises(WebSocketError) as ctx:
        build_close_frame(1000, b'\x80\x80', noheader=False)
    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_build_close_frame_large_message() -> None:
    large_message = b'a' * 1000
    frame = build_close_frame(1000, large_message, noheader=False)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_edge_case() -> None:
    frame = build_close_frame(3000, b'Edge Case', noheader=False)
    assert frame is not None
    assert len(frame) > 0