import asyncio
import pytest
from aiohttp.http_parser import HttpRequestParser
from aiohttp.base_protocol import BaseProtocol

@pytest.mark.parametrize("method, path, expected_eof", [
    ("POST", "/test", True),
    ("GET", "/test", True),
    ("PUT", "/test", True),
    ("DELETE", "/test", True),
])
def test_parse_with_different_methods(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    request_cls: Type[HttpRequestParser],
    method: str,
    path: str,
    expected_eof: bool
) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    text = f"{method} {path} HTTP/1.1\r\n\r\n".encode('utf-8')
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof() == expected_eof

@pytest.mark.parametrize("method, path, headers", [
    ("POST", "/test", {"Content-Length": "0"}),
    ("GET", "/test", {"Transfer-Encoding": "chunked"}),
])
def test_parse_with_headers(
    loop: asyncio.AbstractEventLoop,
    protocol: BaseProtocol,
    request_cls: Type[HttpRequestParser],
    method: str,
    path: str,
    headers: Dict[str, str]
) -> None:
    parser = request_cls(protocol, loop, limit=2**16)
    header_lines = "\r\n".join(f"{k}: {v}" for k, v in headers.items())
    text = f"{method} {path} HTTP/1.1\r\n{header_lines}\r\n\r\n".encode('utf-8')
    msg, payload = parser.feed_data(text)[0][0]

    assert payload.is_eof()