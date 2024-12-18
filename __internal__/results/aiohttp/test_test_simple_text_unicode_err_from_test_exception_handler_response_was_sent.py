import pytest
import struct
from aiohttp.http import WebSocketError, WSCloseCode, WSMsgType
from aiohttp._websocket.reader import WebSocketReader
from aiohttp._websocket.helpers import build_frame

@pytest.fixture
def parser(out: WebSocketDataQueue) -> WebSocketReader:
    return WebSocketReader(out, 256, compress=False)

def test_empty_message(parser: WebSocketReader) -> None:
    data = build_frame(b"", WSMsgType.TEXT)
    parser._feed_data(data)
    assert parser._frame_payload == b""

def test_message_too_large(parser: WebSocketReader) -> None:
    data = build_frame(b"x" * 300, WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_invalid_opcode(parser: WebSocketReader) -> None:
    data = struct.pack("!BB", 0b11111111, 0b00000001) + b"test"
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.PROTOCOL_ERROR

def test_compressed_message(parser: WebSocketReader) -> None:
    data = build_frame(b"hello", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    assert parser._frame_payload == b"hello"

def test_noheader_message(parser: WebSocketReader) -> None:
    data = build_frame(b"test", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    assert parser._frame_payload == b"test"