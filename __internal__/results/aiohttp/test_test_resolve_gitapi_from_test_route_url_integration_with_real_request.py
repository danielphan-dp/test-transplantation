import asyncio
import random
import string
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_creation() -> None:
    req = _mock_request("POST", "/test/path")
    
    assert req.method == "POST"
    assert req.path == "/test/path"
    assert req.version == HttpVersion(1, 1)
    assert req.keep_alive is True
    assert req.headers == CIMultiDict()
    assert req.raw_headers == ()
    
    # Test with custom headers
    headers = CIMultiDict({"Content-Type": "application/json"})
    req_with_headers = _mock_request("GET", "/test/path", headers=headers)
    
    assert req_with_headers.headers == headers
    assert req_with_headers.raw_headers == ((b"Content-Type", b"application/json"),)

@pytest.mark.asyncio
async def test_mock_request_invalid_method() -> None:
    with pytest.raises(ValueError):
        _mock_request("INVALID_METHOD", "/test/path")

@pytest.mark.asyncio
async def test_mock_request_empty_path() -> None:
    req = _mock_request("GET", "")
    assert req.path == ""
    assert req.path_qs == ""

@pytest.mark.asyncio
async def test_mock_request_with_query_string() -> None:
    req = _mock_request("GET", "/test/path?a=1&b=2")
    assert req.query_string == "a=1&b=2"
    assert req.query.get("a") == "1"
    assert req.query.get("b") == "2"

@pytest.mark.asyncio
async def test_mock_request_randomized_requests(loop: asyncio.AbstractEventLoop) -> None:
    alnums = string.ascii_letters + string.digits
    requests = []
    
    for _ in range(100):
        owner = "".join(random.sample(alnums, 10))
        repo = "".join(random.sample(alnums, 10))
        pull_number = random.randint(0, 250)
        requests.append(
            _mock_request(
                method="GET", path=f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
            )
        )

    app = web.Application()
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="OK")

    app.router.add_get("/repos/{owner}/{repo}/pulls/{pull_number}/reviews", handler)
    app.freeze()
    router = app.router

    async def run_requests() -> None:
        for request in requests:
            await router.resolve(request)

    await run_requests()