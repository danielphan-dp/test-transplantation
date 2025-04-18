# This test file was generated from tests/test_app.py in the donor code to test sanic/app.py in the host code through test transplantation.

from __future__ import annotations

import asyncio
from typing import NoReturn
from unittest.mock import AsyncMock

import pytest
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.testing import SanicTestClient

TEST_RESPONSE = HTTPResponse("")


class SimpleError(Exception):
    pass


def test_endpoint_overwrite() -> None:
    app = Sanic("test_app")

    def route(request):
        return HTTPResponse("")

    def route2(request):
        return HTTPResponse("")

    async def route3(request):
        return HTTPResponse("")

    app.add_route(route, "/a", methods=["GET"], name="index")
    app.add_route(route, "/a/a", methods=["GET"], name="index")  # Should not assert, as same view func
    with pytest.raises(SanicException):
        app.add_route(route2, "/a/b", methods=["GET"], name="index")
    app.add_route(route3, "/b", methods=["GET"], name="async")
    app.add_route(route3, "/b/a", methods=["GET"], name="async")  # Should not assert, as same view func
    with pytest.raises(SanicException):
        app.add_route(route2, "/b/b", methods=["GET"], name="async")


@pytest.mark.parametrize(
    "methods, expected_methods",
    [
        (["GET"], {"GET", "HEAD"}),
        (["GET", "OPTIONS"], {"GET", "HEAD", "OPTIONS"}),
    ],
)
def test_add_route_methods(methods, expected_methods) -> None:
    app = Sanic("test_app")

    def route(request):
        return HTTPResponse("")

    app.add_route(route, "/", methods=methods)
    route = app.router.routes_all[0]
    assert set(route.methods) == expected_methods


async def test_host_matching() -> None:
    app = Sanic("test_app")

    @app.route("/", host="quart.com")
    async def route(request):
        return HTTPResponse("")

    test_client = SanicTestClient(app)
    request, response = await test_client.get("/", headers={"host": "quart.com"})
    assert response.status == 200

    request, response = await test_client.get("/", headers={"host": "localhost"})
    assert response.status == 404


@pytest.mark.parametrize(
    "result, expected, raises",
    [
        (None, None, True),
        (TEST_RESPONSE, TEST_RESPONSE, False),
        (("hello", {"X-Header": "bob"}), HTTPResponse("hello", headers={"X-Header": "bob"}), False),
        (("hello", 201), HTTPResponse("hello", status=201), False),
        (("hello", 201, {"X-Header": "bob"}), HTTPResponse("hello", status=201, headers={"X-Header": "bob"}), False),
        (int, None, True),
    ],
)
async def test_make_response(result, expected, raises) -> None:
    app = Sanic("test_app")

    try:
        response = await app._make_response(result)
    except TypeError:
        if not raises:
            raise
    else:
        assert response.headers == expected.headers
        assert response.status == expected.status
        assert response.body == expected.body


@pytest.fixture(name="basic_app")
def _basic_app() -> Sanic:
    app = Sanic("test_app")

    @app.route("/")
    async def route(request):
        return HTTPResponse("")

    @app.route("/exception/")
    async def exception(request):
        raise Exception()

    return app


async def test_app_route_exception(basic_app: Sanic) -> None:
    test_client = SanicTestClient(basic_app)
    request, response = await test_client.get("/exception/")
    assert response.status == 500


async def test_app_before_request_exception(basic_app: Sanic) -> None:
    @basic_app.on_request
    async def before(request):
        raise Exception()

    test_client = SanicTestClient(basic_app)
    request, response = await test_client.get("/")
    assert response.status == 500


async def test_app_after_request_exception(basic_app: Sanic) -> None:
    @basic_app.on_response
    async def after(request, response):
        raise Exception()

    test_client = SanicTestClient(basic_app)
    request, response = await test_client.get("/")
    assert response.status == 500


async def test_app_handle_request_asyncio_cancelled_error() -> None:
    app = Sanic("test_app")

    @app.route("/")
    async def index(request):
        raise asyncio.CancelledError()

    request = Request(b"", app, "GET", "/", None, None, None, None, None, None)
    with pytest.raises(asyncio.CancelledError):
        await app.handle_request(request)


@pytest.mark.parametrize(
    "debug, testing, raises",
    [
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
async def test_propagation(debug: bool, testing: bool, raises: bool) -> None:
    app = Sanic("test_app")

    @app.route("/")
    async def exception(request):
        raise SimpleError()

    app.config.DEBUG = debug
    app.config.TESTING = testing
    test_client = SanicTestClient(app)

    if raises:
        with pytest.raises(SimpleError):
            request = Request(b"", app, "GET", "/", None, None, None, None, None, None)
            await app.handle_request(request)
    else:
        request, response = await test_client.get("/")
        assert response.status == 500