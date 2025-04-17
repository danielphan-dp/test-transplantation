import asyncio
import string
import random
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

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.mark.asyncio
async def test_mock_request_get(app: web.Application):
    request = _mock_request("GET", "/test/path")
    assert request.method == "GET"
    assert request.path == "/test/path"
    assert request.version == HttpVersion(1, 1)

@pytest.mark.asyncio
async def test_mock_request_post(app: web.Application):
    request = _mock_request("POST", "/test/path")
    assert request.method == "POST"
    assert request.path == "/test/path"

@pytest.mark.asyncio
async def test_mock_request_with_query_params(app: web.Application):
    request = _mock_request("GET", "/test/path?a=1&b=2")
    assert request.query_string == "a=1&b=2"
    assert request.path_qs == "/test/path?a=1&b=2"

@pytest.mark.asyncio
async def test_mock_request_invalid_method(app: web.Application):
    request = _mock_request("INVALID", "/test/path")
    assert request.method == "INVALID"
    assert request.path == "/test/path"

@pytest.mark.asyncio
async def test_mock_request_empty_path(app: web.Application):
    request = _mock_request("GET", "")
    assert request.path == ""
    assert request.method == "GET"

@pytest.mark.asyncio
async def test_mock_request_random_requests(app: web.Application):
    alnums = string.ascii_letters + string.digits
    requests = []
    for _ in range(10):
        owner = "".join(random.sample(alnums, 10))
        repo = "".join(random.sample(alnums, 10))
        pull_number = random.randint(0, 250)
        requests.append(
            _mock_request(
                method="GET", path=f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
            )
        )
    
    for request in requests:
        assert request.method == "GET"
        assert request.path.startswith("/repos/")