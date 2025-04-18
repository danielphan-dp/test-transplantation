# This test file was generated from tests/test_app.py in the donor project to test sanic/app.py in the host project through test transplantation.

from __future__ import annotations

import asyncio
from typing import NoReturn
from unittest.mock import AsyncMock

import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException
from sanic_testing.testing import SanicTestClient

TEST_RESPONSE = text("")


class SimpleError(Exception):
    pass


def test_endpoint_overwrite() -> None:
    app = Sanic("test_app")

    @app.route("/a", methods=["GET"])
    def route(request):
        return text("")

    @app.route("/a/a", methods=["GET"])
    def route2(request):
        return text("")

    with pytest.raises(SanicException):
        @app.route("/a/b", methods=["GET"])
        def route3(request):
            return text("")


@pytest.mark.parametrize(
    "methods, expected_methods",
    [
        (["GET"], {"GET", "HEAD"}),
        (["POST"], {"POST"}),
        (["PUT", "DELETE"], {"PUT", "DELETE"}),
    ],
)
def test_add_route_methods(methods: list[str], expected_methods: set[str]) -> None:
    app = Sanic("test_app")

    @app.route("/", methods=methods)
    def route(request):
        return text("")

    route = app.router.routes_all[0]
    assert set(route.methods) == expected_methods


async def test_host_matching() -> None:
    app = Sanic("test_app")

    @app.route("/", host="quart.com")
    async def route(request):
        return text("")

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
        (("hello", {"X-Header": "bob"}), text("hello", headers={"X-Header": "bob"}), False),
        (("hello", 201), text("hello", status=201), False),
        (int, None, True),
    ],
)
async def test_make_response(result, expected, raises: bool) -> None:
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
        return text("")

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

    test_client = SanicTestClient(app)
    with pytest.raises(asyncio.CancelledError):
        request, response = await test_client.get("/")


@pytest.mark.parametrize(
    "debug, raises",
    [
        (False, False),
        (True, True),
    ],
)
async def test_propagation(debug: bool, raises: bool) -> None:
    app = Sanic("test_app")

    @app.route("/")
    async def exception(request):
        raise SimpleError()

    app.config.DEBUG = debug
    test_client = SanicTestClient(app)

    if raises:
        with pytest.raises(SimpleError):
            request, response = await test_client.get("/")
    else:
        request, response = await test_client.get("/")
        assert response.status == 500