import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method(aiohttp_client):
    """Test the close method of the WebSocketResponse."""
    
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
async def test_close_method_not_closed(aiohttp_client):
    """Test that close method sets closed state correctly."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert not ws.closed
        await ws.close()
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_method_multiple_closes(aiohttp_client):
    """Test that multiple calls to close do not raise errors."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.close()
        await ws.close()  # Call close again
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_method_with_message(aiohttp_client):
    """Test that close method can be called with a message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close(code=1000, message="Normal Closure")
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.closed is True
        assert ws.close_code == 1000  # Normal Closure code
        assert ws.close_reason == "Normal Closure"