import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_when_not_closed(aiohttp_client: AiohttpClient) -> None:
    """Test close method when the connector is not already closed."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate the connector's state
    connector = client._connector
    assert not connector.closed
    
    connector.close()
    
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_when_already_closed(aiohttp_client: AiohttpClient) -> None:
    """Test close method when the connector is already closed."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    connector = client._connector
    connector.close()
    
    # Attempt to close again
    connector.close()
    
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test close method while there are active requests."""
    app = web.Application()
    payload = b"test"
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(body=payload)
    
    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector.closed
    
    # Simulate an active request
    await client.get("/")
    
    connector.close()
    
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(aiohttp_client: AiohttpClient) -> None:
    """Test close method with exception handling."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    connector = client._connector
    assert not connector.closed
    
    try:
        connector.close()
    except Exception as e:
        pytest.fail(f"Closing connector raised an exception: {e}")
    
    assert connector.closed