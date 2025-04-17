import pytest
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WebSocketError, WSCloseCode
from aiohttp.http_websocket import WebSocketReader

def test_close_frame_invalid_code(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=999)  # Invalid close code

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_empty_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'')  # Valid close code with empty message

    try:
        parser._feed_data(data)
    except WebSocketError:
        pytest.fail("WebSocketError raised unexpectedly!")

def test_close_frame_large_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    large_message = b'a' * 1000  # Large message
    data = build_close_frame(code=1000, message=large_message)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_invalid_utf8_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    invalid_utf8_message = b'\x80\x81'  # Invalid UTF-8 sequence
    data = build_close_frame(code=1000, message=invalid_utf8_message)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT

def test_close_frame_noheader(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'Normal closure', noheader=True)

    try:
        parser._feed_data(data)
    except WebSocketError:
        pytest.fail("WebSocketError raised unexpectedly!")