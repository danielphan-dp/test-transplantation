import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_on_open_connector(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an open connector."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Simulate opening a connection
    resp = await client.get("/")
    assert resp.status == 200
    await resp.read()
    
    # Close the client and check if it is closed
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_on_already_closed_connector(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an already closed connector."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Close the client
    await client.close()
    assert client.closed
    
    # Attempt to close again and ensure no errors are raised
    await client.close()

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate a long-running request
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Start a request
    task = asyncio.create_task(client.get("/"))
    
    # Close the client while the request is still active
    await client.close()
    
    # Ensure the task is still running
    assert not task.done()
    
    # Wait for the task to complete
    await task
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with exception handling."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        raise Exception("Simulated error")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Attempt to make a request that raises an exception
    with pytest.raises(Exception, match="Simulated error"):
        await client.get("/")
    
    # Close the client after the exception
    await client.close()
    assert client.closed