import pytest
from aiohttp._websocket.helpers import build_close_frame
from aiohttp.http import WebSocketError, WSCloseCode
from aiohttp.http_websocket import WebSocketReader
from aiohttp._websocket.reader import WebSocketDataQueue

def test_close_frame_invalid_code(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=4000)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_empty_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, message=b'')

    try:
        parser._feed_data(data)
    except WebSocketError as ctx:
        assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_large_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    large_message = b'a' * 1000
    data = build_close_frame(code=1000, message=large_message)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_noheader(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_close_frame(code=1000, noheader=True)

    try:
        parser._feed_data(data)
    except WebSocketError as ctx:
        assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_close_frame_invalid_utf8_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    invalid_utf8_message = b'\x80\x81'
    data = build_close_frame(code=1000, message=invalid_utf8_message)

    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)

    assert ctx.value.code == WSCloseCode.INVALID_TEXT