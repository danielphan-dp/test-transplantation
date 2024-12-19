import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_client_close_method(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test the close method of the aiohttp client."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    response = await client.get("/")
    assert response.status == 200
    await client.close()

    with pytest.raises(RuntimeError):
        await client.get("/")  # Ensure that the client cannot be used after closing

@pytest.mark.asyncio
async def test_client_close_multiple_times(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing the client multiple times."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    await client.close()
    await client.close()  # Closing again should not raise an error

@pytest.mark.asyncio
async def test_client_close_with_active_requests(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing the client while there are active requests."""
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.1)  # Simulate a delay
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    task = asyncio.create_task(client.get("/"))
    await asyncio.sleep(0.05)  # Allow the request to start
    await client.close()  # Close the client while the request is in progress
    response = await task  # Wait for the request to complete
    assert response.status == 200  # Ensure the request still completes successfully

@pytest.mark.asyncio
async def test_client_close_no_requests(loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> None:
    """Test closing the client without any active requests."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    client = await aiohttp_client(app)
    await client.close()  # Close the client without making any requests
    # No assertions needed, just ensure it does not raise an error