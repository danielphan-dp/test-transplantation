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
async def test_close_with_message(aiohttp_client):
    """Test closing the WebSocketResponse with a close message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close(code=1000, message="Normal Closure")
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.close_code == 1000
        assert ws.close_reason == "Normal Closure"

@pytest.mark.asyncio
async def test_close_without_opening(aiohttp_client):
    """Test closing the WebSocketResponse without opening it."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        return ws  # Do not prepare or close

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        with pytest.raises(RuntimeError):
            await ws.close()  # Should raise an error since it's not opened

@pytest.mark.asyncio
async def test_close_after_send(aiohttp_client):
    """Test closing the WebSocketResponse after sending a message."""
    
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