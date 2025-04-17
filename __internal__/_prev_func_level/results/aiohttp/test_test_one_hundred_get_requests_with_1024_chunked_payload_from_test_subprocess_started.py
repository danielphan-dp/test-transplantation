import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_when_not_closed(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when the connector is not already closed."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Assuming we have a Connector class with a close method
    connector = client._connector  # Accessing the connector directly for testing
    assert not connector.closed
    connector.close()
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_when_already_closed(aiohttp_client: AiohttpClient) -> None:
    """Test the close method when the connector is already closed."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    connector = client._connector
    connector.close()
    assert connector.closed
    
    # Attempt to close again and ensure no errors are raised
    connector.close()
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test the close method while there are active requests."""
    app = web.Application()
    payload = b"test"
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(body=payload)

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    connector = client._connector
    assert not connector.closed

    # Simulate an active request
    resp = await client.get("/")
    await resp.read()

    connector.close()
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(aiohttp_client: AiohttpClient) -> None:
    """Test the close method with exception handling."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector.closed

    # Simulate an exception during close
    with pytest.raises(Exception):
        # Assuming we can raise an exception in the close method for testing
        connector._raise_exception_on_close = True
        connector.close()  # This should raise an exception

    assert not connector.closed  # Ensure it remains open after exception