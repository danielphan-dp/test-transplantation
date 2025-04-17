import pytest
import struct
from aiohttp._websocket.helpers import build_frame
from aiohttp.http import WSMsgType
from aiohttp.http_websocket import WebSocketReader
from aiohttp.http import WebSocketError, WSCloseCode

@pytest.fixture
def out():
    return WebSocketDataQueue()

@pytest.fixture
def parser(out):
    return WebSocketReader(out, 256, compress=False)

def test_empty_message(out, parser):
    data = build_frame(b"", WSMsgType.TEXT)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == ""
    assert res.size == 0

def test_message_too_large(out, parser):
    data = build_frame(b"text" * 300, WSMsgType.TEXT)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_compressed_message(out, parser):
    data = build_frame(b"text", WSMsgType.TEXT, compress=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == "text"
    assert res.size == 4

def test_noheader_option(out, parser):
    data = build_frame(b"text", WSMsgType.TEXT, noheader=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == "text"
    assert res.size == 4

def test_masked_message(out, parser):
    data = build_frame(b"text", WSMsgType.TEXT, use_mask=True)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == "text"
    assert res.size == 4

def test_fin_flag_false(out, parser):
    data = build_frame(b"text", WSMsgType.TEXT, is_fin=False)
    parser._feed_data(data)
    res = out._buffer[0]
    assert res.data == "text"
    assert res.size == 4

def test_large_message_with_fin(out, parser):
    data = build_frame(b"text" * 300, WSMsgType.TEXT, is_fin=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_large_message_without_fin(out, parser):
    data = build_frame(b"text" * 300, WSMsgType.TEXT, is_fin=False)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG

def test_compressed_large_message(out, parser):
    data = build_frame(b"aaa" * 300, WSMsgType.TEXT, compress=True)
    with pytest.raises(WebSocketError) as ctx:
        parser._feed_data(data)
    assert ctx.value.code == WSCloseCode.MESSAGE_TOO_BIG