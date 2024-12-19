import asyncio
import pytest
from aiohttp.base_protocol import BaseProtocol
from aiohttp.http_parser import HttpResponseParser

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS)
def test_parse_payload_response_with_empty_body(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    text = b"HTTP/1.1 204 No Content\r\ncontent-length: 0\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS)
def test_parse_payload_response_with_invalid_status(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=False)
    text = b"HTTP/1.1 999 Invalid Status\r\ncontent-length: 10\r\n\r\n"
    with pytest.raises(ValueError):
        parser.feed_data(text)

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS)
def test_parse_payload_response_with_large_body(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    body = b"A" * (2**20)  # 1 MB body
    text = f"HTTP/1.1 200 OK\r\ncontent-length: {len(body)}\r\n\r\n".encode() + body
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()
    assert payload.data == body

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS)
def test_parse_payload_response_with_chunked_transfer_encoding(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    text = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n4\r\nWiki\r\n5\r\npedia\r\n0\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()
    assert payload.data == b"Wikipedia"