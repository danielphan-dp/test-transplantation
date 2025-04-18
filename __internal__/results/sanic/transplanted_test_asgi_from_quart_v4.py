# Transplanted from tests/test_asgi.py to test the functionality in sanic/app.py

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.app import ASGIApp

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.asyncio
async def test_handle_request(app):
    # Test that the handle_request method processes a request correctly
    request = Mock(spec=Request)
    request.path = "/"
    request.method = "GET"
    request.headers = {"host": "localhost"}
    request.stream = None
    request.responded = False

    async def handler(request):
        return HTTPResponse("Hello, world!")

    app.router.add("/", handler, methods=["GET"])

    await app.handle_request(request)
    assert request.responded

@pytest.mark.asyncio
async def test_handle_exception(app):
    # Test that the handle_exception method handles exceptions correctly
    request = Mock(spec=Request)
    request.path = "/"
    request.method = "GET"
    request.headers = {"host": "localhost"}
    request.stream = None

    async def handler(request):
        raise ValueError("An error occurred")

    app.router.add("/", handler, methods=["GET"])

    with pytest.raises(ValueError):
        await app.handle_request(request)

@pytest.mark.asyncio
async def test_dispatch_event(app):
    # Test that the dispatch method correctly dispatches events
    event_name = "test.event"
    mock_handler = AsyncMock()

    @app.signal(event_name)
    async def handle_event(**context):
        await mock_handler(**context)

    await app.dispatch(event_name, context={"key": "value"})
    mock_handler.assert_called_once_with(key="value")

@pytest.mark.asyncio
async def test_asgi_lifespan(app):
    # Test that the ASGI lifespan events are handled correctly
    asgi_app = ASGIApp(app)

    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        assert message["type"] == "lifespan.startup.complete"

    await asgi_app({"type": "lifespan"}, receive, send)

@pytest.mark.asyncio
async def test_websocket_handler(app):
    # Test that the websocket handler processes messages correctly
    request = Mock(spec=Request)
    request.path = "/ws"
    request.method = "GET"
    request.headers = {"host": "localhost"}
    request.stream = None

    async def websocket_handler(request, ws):
        await ws.send("Hello, WebSocket!")

    app.router.add("/ws", websocket_handler, methods=["GET"], websocket=True)

    # Mock WebSocket connection
    ws = Mock()
    ws.send = AsyncMock()

    await app._websocket_handler(websocket_handler, request, ws)
    ws.send.assert_called_once_with("Hello, WebSocket!")