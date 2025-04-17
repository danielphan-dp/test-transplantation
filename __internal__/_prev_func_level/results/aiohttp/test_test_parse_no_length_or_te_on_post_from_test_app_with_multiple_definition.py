import asyncio
import pytest
from aiohttp.http_parser import HttpRequestParser
from aiohttp.base_protocol import BaseProtocol

@pytest.mark.parametrize("text, expected_eof", [
    (b"POST /test HTTP/1.1\r\n\r\n", True),
    (b"POST /test HTTP/1.1\r\nContent-Length: 0\r\n\r\n", True),
    (b"POST /test HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n", False),
])
def test_parse_various_payloads(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    request_cls: Type[HttpRequestParser],
    text: bytes,
    expected_eof: bool
) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof() == expected_eof

@pytest.mark.parametrize("text", [
    b"GET /test HTTP/1.1\r\nHost: example.com\r\n\r\n",
    b"POST /test HTTP/1.1\r\nContent-Length: 5\r\n\r\nHello",
])
def test_parse_with_headers(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    request_cls: Type[HttpRequestParser],
    text: bytes
) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    msg, payload = parser.feed_data(text)[0][0]

    assert msg.headers["Host"] == "example.com" if b"Host" in text else "example.com"
    assert not payload.is_eof() if b"Content-Length" in text else payload.is_eof()