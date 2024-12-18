import pytest
from unittest import mock
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.reader import WebSocketReader
from aiohttp.tests.test_websocket_parser import WebSocketDataQueue

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
    out = WebSocketDataQueue()
    parser = WebSocketReader(out, 0, compress=False)
    with mock.patch.object(parser, "parse_frame", autospec=True) as m:
        m.return_value = [
            (0, WSMsgType.CLOSE, build_close_frame(1, b"test", noheader=True), False),
        ]

        with pytest.raises(WebSocketError) as ctx:
            parser._feed_data(b"")

        assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_build_close_frame_large_message() -> None:
    frame = build_close_frame(1000, b"x" * 1000)
    assert frame is not None
    assert len(frame) > 0

def test_build_close_frame_invalid_utf8_message() -> None:
    with pytest.raises(UnicodeDecodeError):
        build_close_frame(1000, b'\x80\x81')  # Invalid UTF-8 sequence