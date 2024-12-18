import asyncio
import random
import string
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

def test_mock_request_creation() -> None:
    """Test the creation of a mock request using _mock_request."""
    
    method = "POST"
    path = "/test/path"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path
    assert request.version == HttpVersion(1, 1)
    assert isinstance(request.headers, CIMultiDictProxy)
    assert request.keep_alive is True

def test_mock_request_with_headers() -> None:
    """Test the creation of a mock request with custom headers."""
    
    method = "GET"
    path = "/test/path"
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method, path)

    request.headers = headers

    assert request.headers.get("Content-Type") == "application/json"

def test_mock_request_invalid_method() -> None:
    """Test the behavior of _mock_request with an invalid HTTP method."""
    
    method = "INVALID"
    path = "/test/path"
    
    with pytest.raises(ValueError):
        _mock_request(method, path)

def test_mock_request_randomized_requests(loop: asyncio.AbstractEventLoop) -> None:
    """Test the resolution of multiple randomized mock requests."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="OK")

    app = web.Application()
    app.router.add_route('*', '/{tail:.*}', handler)
    app.freeze()
    router = app.router

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

    async def run_url_dispatcher() -> None:
        for request in requests:
            await router.resolve(request)

    loop.run_until_complete(run_url_dispatcher())