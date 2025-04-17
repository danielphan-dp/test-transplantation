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
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_method_multiple_calls(aiohttp_client: AiohttpClient) -> None:
    """Test multiple calls to close method."""
    
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
        assert ws.closed is True
        await ws.close()  # Calling close again should not raise an error

@pytest.mark.asyncio
async def test_close_method_with_message(aiohttp_client: AiohttpClient) -> None:
    """Test close method with a message sent before closing."""
    
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
        await ws.close()
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_method_after_send(aiohttp_client: AiohttpClient) -> None:
    """Test close method after sending a message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_str("Test message")
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Another message")
        await ws.close()
        assert ws.closed is True

@pytest.mark.asyncio
async def test_close_method_with_timeout(aiohttp_client: AiohttpClient) -> None:
    """Test close method with a timeout."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(timeout=0.1)
        await ws.prepare(request)
        await ws.close()
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await asyncio.sleep(0.2)  # Ensure we exceed the timeout
        await ws.close()
        assert ws.closed is True