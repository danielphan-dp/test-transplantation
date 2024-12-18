import asyncio
import pytest
from unittest import mock
from multidict import CIMultiDictProxy
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_get():
    request = _mock_request(method="GET", path="/test")
    assert request.method == "GET"
    assert request.path == "/test"

@pytest.mark.asyncio
async def test_mock_request_post():
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request(method="INVALID", path="/error")
    assert request.method == "INVALID"
    assert request.path == "/error"

@pytest.mark.asyncio
async def test_resolve_gitapi_root_with_invalid_path(loop: asyncio.AbstractEventLoop, benchmark: BenchmarkFixture, github_urls: list[str]) -> None:
    async def handler(request: web.Request) -> NoReturn:
        assert False

    app = web.Application()
    for url in github_urls:
        app.router.add_get(url, handler)
    app.freeze()
    router = app.router

    request = _mock_request(method="GET", path="/invalid")

    async def run_url_dispatcher_benchmark() -> Optional[web.UrlMappingMatchInfo]:
        ret = None
        for i in range(250):
            ret = await router.resolve(request)
        return ret

    ret = loop.run_until_complete(run_url_dispatcher_benchmark())
    assert ret is None

@pytest.mark.asyncio
async def test_resolve_gitapi_root_with_empty_path(loop: asyncio.AbstractEventLoop, benchmark: BenchmarkFixture, github_urls: list[str]) -> None:
    async def handler(request: web.Request) -> NoReturn:
        assert False

    app = web.Application()
    for url in github_urls:
        app.router.add_get(url, handler)
    app.freeze()
    router = app.router

    request = _mock_request(method="GET", path="")

    async def run_url_dispatcher_benchmark() -> Optional[web.UrlMappingMatchInfo]:
        ret = None
        for i in range(250):
            ret = await router.resolve(request)
        return ret

    ret = loop.run_until_complete(run_url_dispatcher_benchmark())
    assert ret is None