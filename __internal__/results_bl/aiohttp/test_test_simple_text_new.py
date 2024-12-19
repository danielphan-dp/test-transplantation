import pytest
import random
import zlib
from aiohttp._websocket.helpers import PACK_LEN1, PACK_LEN2, PACK_LEN3, websocket_mask
from aiohttp.http.WSMsgType import TEXT, BINARY
from aiohttp.http_websocket import WebSocketReader, WSMessageText, WSMessageBinary

def test_empty_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"", WSMsgType.TEXT)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res == WSMessageText(data="", size=0, extra="")

def test_large_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    large_data = b"x" * (1 << 16)  # 65536 bytes
    data = build_frame(large_data, WSMsgType.TEXT)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == large_data
    assert res.size == len(large_data)

def test_message_with_mask(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"masked", WSMsgType.TEXT, use_mask=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data != b"masked"  # The data should be masked
    assert res.size == 6

def test_no_header(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"no header", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"no header"
    assert res.size == 9

def test_compressed_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"compressed", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"compressed"
    assert res.size == len(b"compressed")

def test_fin_flag_false(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"not fin", WSMsgType.TEXT, is_fin=False)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == b"not fin"
    assert res.size == 7

def test_binary_message(out: WebSocketDataQueue, parser: WebSocketReader) -> None:
    data = build_frame(b"\x00\x01\x02\x03", WSMsgType.BINARY)
    parser._feed_data(data)
    res = out._buffer[0]
    assert isinstance(res, WSMessageBinary)
    assert res.data == b"\x00\x01\x02\x03"
    assert res.size == 4