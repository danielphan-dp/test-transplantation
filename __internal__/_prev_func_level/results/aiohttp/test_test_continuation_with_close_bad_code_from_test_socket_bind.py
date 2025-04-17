import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.reader import WebSocketReader
from aiohttp._websocket.models import WebSocketDataQueue

def test_build_close_frame_valid_code() -> None:
    frame = build_close_frame(1000, b"Normal Closure")
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_invalid_code() -> None:
    with pytest.raises(ValueError):
        build_close_frame(999, b"Invalid Code")

def test_build_close_frame_empty_message() -> None:
    frame = build_close_frame(1000, b"")
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_noheader() -> None:
    frame = build_close_frame(1000, b"Close without header", noheader=True)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_protocol_error() -> None:
    with mock.patch('aiohttp._websocket.helpers.PACK_CLOSE_CODE', return_value=b'\x03\xe8'):
        with pytest.raises(WebSocketError) as ctx:
            build_close_frame(1, b"test", noheader=True)
        assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_build_close_frame_large_message() -> None:
    large_message = b"x" * 1000
    frame = build_close_frame(1000, large_message)
    assert frame is not None
    assert len(frame) > 0
    assert large_message in frame