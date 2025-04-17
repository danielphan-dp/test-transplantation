import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_on_open_connection(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an open connection."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate opening a connection
    async with client.get("/") as resp:
        assert resp.status == 200
    
    # Close the client and check if it is closed
    await client.close()
    assert client.closed

@pytest.mark.asyncio
async def test_close_method_on_already_closed_connection(aiohttp_client: AiohttpClient) -> None:
    """Test the close method on an already closed connection."""
    app = web.Application()
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
    client = await aiohttp_client(app)
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate a long request
        return web.Response(text="Hello, world")
    
    app.router.add_route("GET", "/", handler)
    
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
async def test_close_method_with_multiple_clients(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with multiple clients."""
    app = web.Application()
    client1 = await aiohttp_client(app)
    client2 = await aiohttp_client(app)
    
    # Close the first client
    await client1.close()
    assert client1.closed
    
    # Close the second client
    await client2.close()
    assert client2.closed