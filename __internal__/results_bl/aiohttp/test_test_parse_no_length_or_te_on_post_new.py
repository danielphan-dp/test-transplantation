import asyncio
import pytest
from aiohttp.base_protocol import BaseProtocol
from aiohttp.http_parser import HttpRequestParser

@pytest.fixture(params=REQUEST_PARSERS, ids=_gen_ids(REQUEST_PARSERS))
def request_cls(request: pytest.FixtureRequest) -> Type[HttpRequestParser]:
    return request.param

def test_parse_empty_post(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, request_cls: Type[HttpRequestParser]) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    text = b"POST /test HTTP/1.1\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()

def test_parse_large_payload(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, request_cls: Type[HttpRequestParser]) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    large_payload = b"A" * (2**16 + 1)
    text = b"POST /test HTTP/1.1\r\nContent-Length: {}\r\n\r\n{}".format(len(large_payload), large_payload)
    msg, payload = parser.feed_data(text)[0][0]

    assert not payload.is_eof()

def test_parse_invalid_method(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, request_cls: Type[HttpRequestParser]) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    text = b"INVALID /test HTTP/1.1\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()

def test_parse_missing_content_length(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, request_cls: Type[HttpRequestParser]) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    text = b"POST /test HTTP/1.1\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()