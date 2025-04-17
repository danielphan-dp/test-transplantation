import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_websocket_connection(aiohttp_client):
    """Test that closing a WebSocket connection works as expected."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_websocket_multiple_times(aiohttp_client):
    """Test that closing a WebSocket connection multiple times does not raise an error."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.close()
        await ws.close()  # Closing again should not raise an error

@pytest.mark.asyncio
async def test_close_websocket_after_send(aiohttp_client):
    """Test that closing a WebSocket after sending a message works correctly."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_str("Hello")
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        msg = await ws.receive()
        assert msg.type == web.WSMsgType.TEXT
        assert msg.data == "Hello"
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_websocket_with_error(aiohttp_client):
    """Test that closing a WebSocket connection when an error occurs is handled gracefully."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        raise Exception("Simulated error")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        with pytest.raises(Exception, match="Simulated error"):
            await ws.receive()
        assert ws.closed is True