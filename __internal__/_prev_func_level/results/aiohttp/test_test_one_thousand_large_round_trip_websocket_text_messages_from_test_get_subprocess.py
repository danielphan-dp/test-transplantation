import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method(aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the WebSocketResponse."""
    
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
        assert ws.closed

@pytest.mark.asyncio
async def test_close_method_multiple_calls(aiohttp_client: AiohttpClient) -> None:
    """Test multiple calls to the close method."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.close()
        with pytest.raises(RuntimeError):
            await ws.close()

@pytest.mark.asyncio
async def test_close_method_with_message(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with a close message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.close(code=1000, message="Normal Closure")
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.closed
        assert ws.close_code == 1000
        assert ws.close_reason == "Normal Closure"