# This test file was generated from tests/test_asgi.py to sanic/asgi.py through test transplantation.

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.exceptions import BadRequest, ServerError
from sanic.models.asgi import ASGIScope, ASGIReceive, ASGISend
from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.asgi import ASGIApp, Lifespan


@pytest.fixture
def sanic_app():
    app = Sanic("test_app")
    return app


@pytest.mark.asyncio
async def test_lifespan_startup(sanic_app):
    # Test that the startup sequence completes without errors
    scope = {"type": "lifespan"}
    receive = AsyncMock()
    send = AsyncMock()
    lifespan = Lifespan(sanic_app, scope, receive, send)

    receive.return_value = {"type": "lifespan.startup"}
    await lifespan()

    send.assert_called_with({"type": "lifespan.startup.complete"})


@pytest.mark.asyncio
async def test_lifespan_shutdown(sanic_app):
    # Test that the shutdown sequence completes without errors
    scope = {"type": "lifespan"}
    receive = AsyncMock()
    send = AsyncMock()
    lifespan = Lifespan(sanic_app, scope, receive, send)

    receive.return_value = {"type": "lifespan.shutdown"}
    await lifespan()

    send.assert_called_with({"type": "lifespan.shutdown.complete"})


@pytest.mark.asyncio
async def test_asgi_app_create(sanic_app):
    # Test the creation of an ASGIApp instance
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "headers": [(b"host", b"sanic")],
        "raw_path": b"/",
        "query_string": b"",
    }
    receive = AsyncMock()
    send = AsyncMock()

    app_instance = await ASGIApp.create(sanic_app, scope, receive, send)

    assert isinstance(app_instance, ASGIApp)
    assert app_instance.sanic_app == sanic_app
    assert app_instance.request.method == "GET"


@pytest.mark.asyncio
async def test_asgi_app_read(sanic_app):
    # Test reading from an ASGI message
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "headers": [(b"host", b"sanic")],
        "raw_path": b"/",
        "query_string": b"",
    }
    receive = AsyncMock()
    send = AsyncMock()

    app_instance = await ASGIApp.create(sanic_app, scope, receive, send)
    app_instance.transport.receive = AsyncMock(
        return_value={"body": b"test", "more_body": False}
    )

    body = await app_instance.read()
    assert body == b"test"


@pytest.mark.asyncio
async def test_asgi_app_respond(sanic_app):
    # Test responding with a BaseHTTPResponse
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "headers": [(b"host", b"sanic")],
        "raw_path": b"/",
        "query_string": b"",
    }
    receive = AsyncMock()
    send = AsyncMock()

    app_instance = await ASGIApp.create(sanic_app, scope, receive, send)
    response = Mock(spec=BaseHTTPResponse)
    response.status = 200
    response.processed_headers = []

    app_instance.stage = app_instance.stage.HANDLER
    app_instance.respond(response)

    assert app_instance.response == response


@pytest.mark.asyncio
async def test_asgi_app_send(sanic_app):
    # Test sending data through ASGIApp
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "headers": [(b"host", b"sanic")],
        "raw_path": b"/",
        "query_string": b"",
    }
    receive = AsyncMock()
    send = AsyncMock()

    app_instance = await ASGIApp.create(sanic_app, scope, receive, send)
    app_instance.transport.send = AsyncMock()

    await app_instance.send("data", end_stream=True)

    app_instance.transport.send.assert_called_with(
        {
            "type": "http.response.body",
            "body": b"data",
            "more_body": False,
        }
    )