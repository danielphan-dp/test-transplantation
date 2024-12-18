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
        assert ws.close_code == 1000
        assert ws.close_reason == "Normal Closure"

@pytest.mark.asyncio
async def test_close_method_after_send(aiohttp_client: AiohttpClient) -> None:
    """Test closing after sending a message."""
    
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
        assert ws.close_code is None

@pytest.mark.asyncio
async def test_close_method_with_timeout(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with a timeout."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(timeout=0.1)
        await ws.prepare(request)
        await asyncio.sleep(0.2)  # Simulate delay
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)
    
    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await asyncio.sleep(0.2)  # Wait for the close to happen
        assert ws.close_code is not None
        assert ws.closed