import pytest
from unittest import mock
from aiohttp.http import WSCloseCode, WebSocketError
from aiohttp._websocket.helpers import build_close_frame, WSMsgType

def test_build_close_frame_valid_code():
    frame = build_close_frame(1000, b"Normal Closure")
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_no_message():
    frame = build_close_frame(1000)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_invalid_code():
    with pytest.raises(ValueError):
        build_close_frame(9999, b"Invalid Code")

def test_build_close_frame_empty_message():
    frame = build_close_frame(1000, b"")
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_noheader():
    frame = build_close_frame(1000, b"Normal Closure", noheader=True)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_protocol_error():
    with mock.patch('aiohttp._websocket.helpers.PACK_CLOSE_CODE', return_value=b'\x03\xe8'):
        with pytest.raises(WebSocketError) as ctx:
            build_close_frame(1, b"test", noheader=True)
        assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR