import pytest
from aiohttp.http import WebSocketError, WSCloseCode
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http_websocket import WebSocketReader

def test_close_frame_invalid_code(parser: WebSocketReader) -> None:
    data = build_close_frame(code=9999, message=b'')
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.INVALID_PAYLOAD

def test_close_frame_empty_message(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'')
    parser._feed_data(data)
    # Assuming a successful close frame should not raise an error
    assert parser._state == 'CLOSED'

def test_close_frame_noheader(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'Normal closure', noheader=True)
    parser._feed_data(data)
    assert parser._state == 'CLOSED'

def test_close_frame_large_message(parser: WebSocketReader) -> None:
    large_message = b'A' * 1234  # Exceeding typical frame size
    data = build_close_frame(code=1000, message=large_message)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.INVALID_PAYLOAD

def test_close_frame_invalid_unicode(parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b"\xf4\x90\x80\x80")
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.INVALID_TEXT