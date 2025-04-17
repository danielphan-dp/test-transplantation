import asyncio
import pytest
from aiohttp.http_parser import HttpRequestParser
from aiohttp.base_protocol import BaseProtocol

@pytest.mark.parametrize("data", [
    b"POST /test HTTP/1.1\r\nContent-Length: 0\r\n\r\n",
    b"POST /test HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n",
    b"POST /test HTTP/1.1\r\nContent-Length: 5\r\n\r\nHello",
    b"POST /test HTTP/1.1\r\n\r\nHello",
])
def test_parse_various_payloads(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    request_cls: Type[HttpRequestParser],
    data: bytes
) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    msg, payload = parser.feed_data(data)[0][0]

    if b"Content-Length" in data or b"Transfer-Encoding" in data:
        assert not payload.is_eof()
    else:
        assert payload.is_eof()