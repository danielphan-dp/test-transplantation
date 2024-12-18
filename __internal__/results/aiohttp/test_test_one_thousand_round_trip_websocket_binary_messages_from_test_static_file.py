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
async def test_close_multiple_times(aiohttp_client):
    """Test closing the WebSocketResponse multiple times."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close()
        await ws.close()  # Closing again
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_with_pending_messages(aiohttp_client):
    """Test closing the WebSocketResponse while there are pending messages."""
    
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
        assert msg.data == "Hello"
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_with_error_handling(aiohttp_client):
    """Test closing the WebSocketResponse with error handling."""
    
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
        with pytest.raises(RuntimeError):
            await ws.send_str("This should fail")