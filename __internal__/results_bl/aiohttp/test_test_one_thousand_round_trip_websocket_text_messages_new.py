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
async def test_close_multiple_times(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing a WebSocket connection multiple times."""
    
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
        await resp.close()

@pytest.mark.asyncio
async def test_close_without_opening(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing a WebSocket connection without opening it."""
    
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
        await resp.close()