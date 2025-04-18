# Transplanted from tests/test_asgi.py to test the functionality in sanic/app.py

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.app import ASGIApp
from sanic.exceptions import SanicException

# Test that the ASGI app can handle HTTP requests correctly
async def test_http_request_handling():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return HTTPResponse("Hello, world!")

    scope = {
        "type": "http",
        "asgi": {},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "query_string": b"",
        "headers": [(b"host", b"localhost")],
        "client": ("127.0.0.1", 80),
        "server": None,
    }

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        assert message["type"] == "http.response.start" or message["type"] == "http.response.body"

    asgi_app = ASGIApp(app, scope, receive, send)
    await asgi_app()

# Test that the ASGI app can handle WebSocket connections correctly
async def test_websocket_handling():
    app = Sanic("test_app")

    @app.websocket("/ws")
    async def handler(request, ws):
        await ws.send("Hello, world!")

    scope = {
        "type": "websocket",
        "asgi": {},
        "http_version": "1.1",
        "scheme": "ws",
        "path": "/ws",
        "query_string": b"",
        "headers": [(b"host", b"localhost")],
        "client": ("127.0.0.1", 80),
        "server": None,
        "subprotocols": [],
    }

    async def receive():
        return {"type": "websocket.connect"}

    async def send(message):
        assert message["type"] == "websocket.accept" or message["type"] == "websocket.send"

    asgi_app = ASGIApp(app, scope, receive, send)
    await asgi_app()

# Test that the app raises an exception for invalid server events
async def test_invalid_server_event():
    app = Sanic("test_app")

    with pytest.raises(SanicException):
        await app._server_event("invalid", "event")

# Test that the app can handle exceptions in request handling
async def test_handle_exception():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        raise ValueError("Test exception")

    scope = {
        "type": "http",
        "asgi": {},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "query_string": b"",
        "headers": [(b"host", b"localhost")],
        "client": ("127.0.0.1", 80),
        "server": None,
    }

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        assert message["type"] == "http.response.start" or message["type"] == "http.response.body"

    asgi_app = ASGIApp(app, scope, receive, send)
    await asgi_app()