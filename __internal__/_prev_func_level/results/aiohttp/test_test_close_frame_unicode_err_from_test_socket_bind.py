import pytest
from aiohttp.http import WebSocketError, WSCloseCode
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http_websocket import WebSocketReader

def test_close_frame_invalid_code(parser: WebSocketReader) -> None:
    data = build_close_frame(code=9999)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_empty_message(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'')

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_close_frame_large_message(parser: WebSocketReader) -> None:
    large_message = b'a' * 1000
    data = build_close_frame(code=1000, message=large_message)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_close_frame_unicode_error(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b"\xf4\x90\x80\x80")

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_close_frame_noheader(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'Normal close', noheader=True)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT