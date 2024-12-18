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

@pytest.mark.asyncio
async def test_mock_request_get(app: web.Application):
    async def handler(request: web.Request):
        return web.Response(text="Hello, World!")

    app.router.add_get("/", handler)

    request = _mock_request(method="GET", path="/")
    response = await app.router.resolve(request)

    assert response is not None
    assert response.get_info()["path"] == "/"

@pytest.mark.asyncio
async def test_mock_request_post(app: web.Application):
    async def handler(request: web.Request):
        return web.Response(text="Posted!")

    app.router.add_post("/post", handler)

    request = _mock_request(method="POST", path="/post")
    response = await app.router.resolve(request)

    assert response is not None
    assert response.get_info()["path"] == "/post"

@pytest.mark.asyncio
async def test_mock_request_invalid_method(app: web.Application):
    async def handler(request: web.Request):
        return web.Response(status=405)

    app.router.add_get("/resource", handler)

    request = _mock_request(method="DELETE", path="/resource")
    response = await app.router.resolve(request)

    assert response is not None
    assert response.status == 405

@pytest.mark.asyncio
async def test_mock_request_with_query_params(app: web.Application):
    async def handler(request: web.Request):
        assert request.query.get("param") == "value"
        return web.Response(text="Query received!")

    app.router.add_get("/query", handler)

    request = _mock_request(method="GET", path="/query?param=value")
    response = await app.router.resolve(request)

    assert response is not None
    assert response.get_info()["path"] == "/query"

@pytest.mark.asyncio
async def test_mock_request_path_with_double_slash(app: web.Application):
    async def handler(request: web.Request):
        return web.Response(text="Double slash!")

    app.router.add_get("/path//to", handler)

    request = _mock_request(method="GET", path="/path//to")
    response = await app.router.resolve(request)

    assert response is not None
    assert response.get_info()["path"] == "/path//to"