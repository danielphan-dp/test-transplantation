import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_websocket_connection(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing a WebSocket connection."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    resp = await client.ws_connect("/")

    await resp.close()
    assert resp.closed is True

@pytest.mark.asyncio
async def test_close_websocket_multiple_closes(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test multiple close calls on a WebSocket connection."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    resp = await client.ws_connect("/")

    await resp.close()
    await resp.close()  # Closing again
    assert resp.closed is True

@pytest.mark.asyncio
async def test_close_websocket_without_open(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing a WebSocket that was never opened."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    resp = await client.ws_connect("/")
    await resp.close()

    with pytest.raises(RuntimeError):
        await resp.close()  # Attempting to close again should raise an error

@pytest.mark.asyncio
async def test_close_websocket_after_message(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing a WebSocket after sending a message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_str("Hello")
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    resp = await client.ws_connect("/")

    msg = await resp.receive()
    assert msg.data == "Hello"
    
    await resp.close()
    assert resp.closed is True