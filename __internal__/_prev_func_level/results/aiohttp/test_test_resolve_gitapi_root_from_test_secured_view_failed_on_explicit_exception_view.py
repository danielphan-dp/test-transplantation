import asyncio
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

def test_mock_request_get(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, World!")

    app.router.add_get("/test", handler)

    request = _mock_request(method="GET", path="/test")

    async def run_request() -> web.Response:
        return await app.router.resolve(request)

    response = asyncio.run(run_request())
    assert response.status == 200
    assert await response.text() == "Hello, World!"

def test_mock_request_post(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Post Received", status=201)

    app.router.add_post("/test", handler)

    request = _mock_request(method="POST", path="/test")

    async def run_request() -> web.Response:
        return await app.router.resolve(request)

    response = asyncio.run(run_request())
    assert response.status == 201
    assert await response.text() == "Post Received"

def test_mock_request_invalid_method(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(status=405)

    app.router.add_get("/test", handler)

    request = _mock_request(method="PUT", path="/test")

    async def run_request() -> web.Response:
        return await app.router.resolve(request)

    response = asyncio.run(run_request())
    assert response.status == 405

def test_mock_request_invalid_path(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/invalid")

    async def run_request() -> web.Response:
        return await app.router.resolve(request)

    response = asyncio.run(run_request())
    assert response is None

def test_mock_request_with_headers(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        assert request.headers.get("X-Custom-Header") == "Value"
        return web.Response(text="Header Received")

    app.router.add_get("/test", handler)

    request = _mock_request(method="GET", path="/test")
    request.headers["X-Custom-Header"] = "Value"

    async def run_request() -> web.Response:
        return await app.router.resolve(request)

    response = asyncio.run(run_request())
    assert response.status == 200
    assert await response.text() == "Header Received"