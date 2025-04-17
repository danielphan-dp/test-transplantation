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
        await ws.send_str("Hello")
        await ws.close()

    assert ws.closed is True
    assert ws.close_code is not None

@pytest.mark.asyncio
async def test_close_method_multiple_closes(aiohttp_client: AiohttpClient) -> None:
    """Test multiple calls to close method."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        await ws.close()
        await ws.close()  # Closing again

    assert ws.closed is True
    assert ws.close_code is not None

@pytest.mark.asyncio
async def test_close_method_with_no_send(aiohttp_client: AiohttpClient) -> None:
    """Test close method without sending any messages."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.close()

    assert ws.closed is True
    assert ws.close_code is not None

@pytest.mark.asyncio
async def test_close_method_after_receive(aiohttp_client: AiohttpClient) -> None:
    """Test close method after receiving a message."""
    
    async def handler(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    async with client.ws_connect("/") as ws:
        await ws.send_str("Hello")
        msg = await ws.receive()
        assert msg.type == web.WSMsgType.TEXT
        await ws.close()

    assert ws.closed is True
    assert ws.close_code is not None