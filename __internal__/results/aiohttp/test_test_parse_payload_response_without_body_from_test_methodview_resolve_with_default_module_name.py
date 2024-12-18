import asyncio
import pytest
from aiohttp.http_parser import HttpResponseParser
from aiohttp.base_protocol import BaseProtocol

@pytest.fixture(params=[True, False], ids=["with_body", "without_body"])
def response_with_body(request):
    return request.param

def test_parse_payload_response_with_body(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    response_cls: Type[HttpResponseParser],
    response_with_body: bool
) -> None:
    body_length = 10 if response_with_body else 0
    text = f"HTTP/1.1 200 Ok\r\ncontent-length: {body_length}\r\n\r\n".encode()
    parser = response_cls(protocol, loop, 2**16, response_with_body=response_with_body)
    msg, payload = parser.feed_data(text)[0][0]

    if response_with_body:
        assert not payload.is_eof()
    else:
        assert payload.is_eof()

def test_parse_payload_response_invalid_status_line(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    response_cls: Type[HttpResponseParser]
) -> None:
    text = b"INVALID STATUS LINE\r\ncontent-length: 10\r\n\r\n"
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)

    with pytest.raises(ValueError):
        parser.feed_data(text)

def test_parse_payload_response_large_content_length(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    response_cls: Type[HttpResponseParser]
) -> None:
    text = b"HTTP/1.1 200 Ok\r\ncontent-length: 1000000\r\n\r\n" + b"x" * 1000000
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    msg, payload = parser.feed_data(text)[0][0]

    assert not payload.is_eof()