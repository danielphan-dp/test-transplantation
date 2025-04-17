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
    assert not connector._closed  # Ensure it's not closed before calling close
    connector.close()
    assert connector._closed  # Ensure it is closed after calling close

@pytest.mark.asyncio
async def test_close_method_when_already_closed(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when the connector is already closed."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    connector.close()  # Close it first
    assert connector._closed  # Ensure it is closed
    
    # Call close again and check for no errors
    connector.close()  # Should not raise any error

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.1)  # Simulate a delay
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector._closed  # Ensure it's not closed before calling close
    
    # Start a request
    response = await client.get("/")
    assert response.status == 200
    
    # Now close the connector
    connector.close()
    assert connector._closed  # Ensure it is closed after calling close

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with exception handling."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        raise Exception("Simulated error")

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector._closed  # Ensure it's not closed before calling close
    
    # Call the handler and catch the exception
    with pytest.raises(Exception):
        await client.get("/")
    
    # Now close the connector
    connector.close()
    assert connector._closed  # Ensure it is closed after calling close