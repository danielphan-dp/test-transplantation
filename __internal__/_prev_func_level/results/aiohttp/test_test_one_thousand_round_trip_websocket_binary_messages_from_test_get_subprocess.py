import asyncio
import pytest
from aiohttp import web
from aiohttp._websocket.helpers import WSMsgType
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_websocket_connection(aiohttp_client):
    """Test closing a WebSocket connection properly."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await close_event.wait()  # Wait until the event is set
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        close_event.set()  # Trigger the close event
        await ws.close()

    assert ws.closed  # Ensure the WebSocket is closed

@pytest.mark.asyncio
async def test_close_websocket_multiple_times(aiohttp_client):
    """Test closing a WebSocket connection multiple times."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await close_event.wait()
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        close_event.set()
        await ws.close()
        await ws.close()  # Close again to test idempotency

    assert ws.closed

@pytest.mark.asyncio
async def test_close_websocket_after_send(aiohttp_client):
    """Test closing a WebSocket connection after sending a message."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await close_event.wait()
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        close_event.set()
        await ws.close()

    assert ws.closed

@pytest.mark.asyncio
async def test_close_websocket_without_response(aiohttp_client):
    """Test closing a WebSocket connection without sending a message."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await close_event.wait()
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        close_event.set()  # Close without sending any message
        await ws.close()

    assert ws.closed

@pytest.mark.asyncio
async def test_close_websocket_with_error_handling(aiohttp_client):
    """Test closing a WebSocket connection with error handling."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await close_event.wait()
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        close_event.set()
        await ws.close()

    assert ws.closed

@pytest.mark.asyncio
async def test_close_websocket_with_timeout(aiohttp_client):
    """Test closing a WebSocket connection with a timeout."""
    close_event = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(timeout=0.1)  # Set a short timeout
        await ws.prepare(request)
        await close_event.wait()
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        close_event.set()
        await ws.close()

    assert ws.closed