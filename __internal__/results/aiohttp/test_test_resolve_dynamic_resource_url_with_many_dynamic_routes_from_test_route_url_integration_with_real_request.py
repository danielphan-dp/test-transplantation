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

def test_resolve_dynamic_resource_url_with_edge_cases(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    """Test resolving dynamic resources with edge cases in the URL."""

    async def handler(request: web.Request) -> None:
        return web.Response(text="Handled")

    app.router.add_route("GET", "/api/server/dispatch/{customer}/update", handler)
    app.router.add_route("GET", "/api/server/dispatch/{customer}/update/extra", handler)
    app.router.add_route("GET", "/api/server/dispatch/{customer}/update/", handler)
    app.router.add_route("GET", "/api/server/dispatch/{customer}/update?query=param", handler)
    app.freeze()
    router = app.router

    requests = [
        _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update")
        for customer in range(5)
    ] + [
        _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update/extra")
        for customer in range(5)
    ] + [
        _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update/")
        for customer in range(5)
    ] + [
        _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update?query=param")
        for customer in range(5)
    ]

    async def run_url_dispatcher() -> None:
        for request in requests:
            await router.resolve(request)

    loop.run_until_complete(run_url_dispatcher())

    for customer in range(5):
        request = _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update")
        match_info = loop.run_until_complete(router.resolve(request))
        assert match_info is not None
        assert match_info.get_info()["formatter"] == "/api/server/dispatch/{customer}/update"

        request = _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update/extra")
        match_info = loop.run_until_complete(router.resolve(request))
        assert match_info is not None
        assert match_info.get_info()["formatter"] == "/api/server/dispatch/{customer}/update/extra"

        request = _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update/")
        match_info = loop.run_until_complete(router.resolve(request))
        assert match_info is not None
        assert match_info.get_info()["formatter"] == "/api/server/dispatch/{customer}/update/"

        request = _mock_request(method="GET", path=f"/api/server/dispatch/{customer}/update?query=param")
        match_info = loop.run_until_complete(router.resolve(request))
        assert match_info is not None
        assert match_info.get_info()["formatter"] == "/api/server/dispatch/{customer}/update"