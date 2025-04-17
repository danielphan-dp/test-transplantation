import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

def test_mock_request_creation(app: web.Application) -> None:
    request = _mock_request(method="POST", path="/api/test")
    assert request.method == "POST"
    assert request.path == "/api/test"
    assert request.version == HttpVersion(1, 1)
    assert request.keep_alive is True

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="GET", path="/api/test")
    request.headers.update(headers)
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_invalid_method(app: web.Application) -> None:
    with pytest.raises(ValueError):
        _mock_request(method="INVALID", path="/api/test")

def test_mock_request_path_with_query(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/api/test?param=value")
    assert request.path_qs == "/api/test?param=value"
    assert request.query_string == "param=value"

def test_resolve_multiple_routes(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    for count in range(5):
        app.router.add_route("GET", f"/api/resource/{count}", handler)

    request = _mock_request(method="GET", path="/api/resource/3")
    
    async def run_url_dispatcher() -> web.UrlMappingMatchInfo:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is not None
    assert ret.get_info()["path"] == "/api/resource/3", ret.get_info()