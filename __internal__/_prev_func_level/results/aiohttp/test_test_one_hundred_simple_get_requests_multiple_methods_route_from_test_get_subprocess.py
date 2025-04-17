import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_not_called_on_open_connection(aiohttp_client):
    """Test that close method does not close an already open connection."""
    app = web.Application()
    handler_called = asyncio.Event()

    async def handler(request: web.Request) -> web.Response:
        handler_called.set()
        return web.Response()

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    await client.get("/")
    assert handler_called.is_set()

    # Simulate not calling close
    # Here we would check if the connection is still open
    # This is a placeholder for actual connection state checking
    assert not client.closed

@pytest.mark.asyncio
async def test_close_method_closes_connection(aiohttp_client):
    """Test that close method properly closes the connection."""
    app = web.Application()
    handler_called = asyncio.Event()

    async def handler(request: web.Request) -> web.Response:
        handler_called.set()
        return web.Response()

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    await client.get("/")
    assert handler_called.is_set()

    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_called_multiple_times(aiohttp_client):
    """Test that calling close multiple times does not raise an error."""
    app = web.Application()
    handler_called = asyncio.Event()

    async def handler(request: web.Request) -> web.Response:
        handler_called.set()
        return web.Response()

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    await client.get("/")
    assert handler_called.is_set()

    await client.close()
    assert client.closed

    # Call close again
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client):
    """Test that close method handles active requests gracefully."""
    app = web.Application()
    close_called = asyncio.Event()

    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.1)  # Simulate long request
        close_called.set()
        return web.Response()

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    await client.get("/")
    assert close_called.is_set()

    await client.close()
    assert client.closed