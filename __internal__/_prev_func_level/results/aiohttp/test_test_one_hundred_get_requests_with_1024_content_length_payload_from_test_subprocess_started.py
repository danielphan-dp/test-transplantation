import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_when_not_closed(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when the connector is not already closed."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Simulate the connector's close method
    connector = client._connector
    assert not connector.closed
    connector.close()
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_when_already_closed(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when the connector is already closed."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    connector.close()
    assert connector.closed
    
    # Attempt to close again
    connector.close()
    assert connector.closed  # Should still be closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate long processing
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    # Start a request
    task = asyncio.create_task(client.get("/"))
    
    # Close the connector while the request is still processing
    connector = client._connector
    connector.close()
    
    # Ensure the task is still running
    await asyncio.sleep(0.1)
    assert not connector.closed  # Should not be closed until the request finishes
    
    response = await task
    await response.read()
    assert connector.closed  # Should be closed after the request is done

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with exception handling."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        raise Exception("Simulated error")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector.closed
    
    try:
        await client.get("/")
    except Exception:
        pass  # Ignore the exception for this test
    
    connector.close()
    assert connector.closed  # Should be closed after handling the exception