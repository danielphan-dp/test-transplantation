# Transplanted from tests/test_sync.py in the donor to test functionality in sanic/app.py

from __future__ import annotations

import threading
from collections.abc import Generator

import pytest

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.testing import SanicTestClient


@pytest.fixture(name="app")
def _app() -> Sanic:
    app = Sanic("test_app")

    @app.route("/", methods=["GET", "POST"])
    async def index(request: Request) -> HTTPResponse:
        return HTTPResponse(request.method)

    @app.route("/gen")
    async def gen(request: Request) -> HTTPResponse:
        def _gen() -> Generator[bytes, None, None]:
            yield b"%d" % threading.current_thread().ident
            for _ in range(2):
                yield b"b"

        return HTTPResponse(body=_gen(), status=200)

    return app


@pytest.fixture(name="test_client")
def _test_client(app: Sanic) -> SanicTestClient:
    return app.test_client


async def test_sync_request_context(test_client: SanicTestClient) -> None:
    request, response = await test_client.get("/")
    assert b"GET" in response.body
    request, response = await test_client.post("/")
    assert b"POST" in response.body


async def test_sync_generator(test_client: SanicTestClient) -> None:
    request, response = await test_client.get("/gen")
    result = response.body
    assert result[-2:] == b"bb"
    assert int(result[:-2]) != threading.current_thread().ident