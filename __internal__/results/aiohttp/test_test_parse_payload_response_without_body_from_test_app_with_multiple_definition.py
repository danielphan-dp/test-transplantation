import asyncio
import pytest
from aiohttp.base_protocol import BaseProtocol
from aiohttp.http_parser import HttpResponseParser

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS, ids=_gen_ids(RESPONSE_PARSERS))
def test_parse_payload_response_with_body(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    text = b"HTTP/1.1 200 Ok\r\ncontent-length: 10\r\n\r\n1234567890"
    msg, payload = parser.feed_data(text)[0][0]

    assert not payload.is_eof()
    assert payload.read() == b"1234567890"
    assert payload.is_eof()  # Ensure EOF is reached after reading

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS, ids=_gen_ids(RESPONSE_PARSERS))
def test_parse_payload_response_with_invalid_length(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    text = b"HTTP/1.1 200 Ok\r\ncontent-length: 5\r\n\r\n1234567890"
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()  # Should be EOF since the length is invalid
    assert payload.read() == b""  # No data should be read

@pytest.mark.parametrize("response_cls", RESPONSE_PARSERS, ids=_gen_ids(RESPONSE_PARSERS))
def test_parse_payload_response_with_chunked_transfer(loop: asyncio.AbstractEventLoop, protocol: BaseProtocol, response_cls: Type[HttpResponseParser]) -> None:
    parser = response_cls(protocol, loop, 2**16, response_with_body=True)
    text = b"HTTP/1.1 200 Ok\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nHello\r\n5\r\nWorld\r\n0\r\n\r\n"
    msg, payload = parser.feed_data(text)[0][0]

    assert not payload.is_eof()
    assert payload.read() == b"HelloWorld"
    assert payload.is_eof()  # Ensure EOF is reached after reading all chunks