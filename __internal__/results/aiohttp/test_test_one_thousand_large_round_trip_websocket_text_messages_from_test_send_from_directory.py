import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_websocket_connection(aiohttp_client):
    """Test closing a WebSocket connection."""
    close_called = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        close_called.set()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        await ws.close()

    await close_called.wait()

@pytest.mark.asyncio
async def test_close_multiple_times(aiohttp_client):
    """Test closing a WebSocket connection multiple times."""
    close_count = 0

    async def handler(request: web.Request) -> web.WebSocketResponse:
        nonlocal close_count
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        close_count += 1
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        await ws.close()
        await ws.close()  # Attempt to close again

    assert close_count == 1

@pytest.mark.asyncio
async def test_close_with_no_messages(aiohttp_client):
    """Test closing a WebSocket connection with no messages sent."""
    close_called = asyncio.Event()

    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        close_called.set()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.close()

    await close_called.wait()