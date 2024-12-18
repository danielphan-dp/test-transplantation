import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

@pytest.mark.asyncio
async def test_close_method_not_called_twice(aiohttp_client: AiohttpClient) -> None:
    """Test that close method can be called only once."""
    app = web.Application()
    client = await aiohttp_client(app)
    
    # Simulate the object that has the close method
    class TestConnector:
        def __init__(self):
            self.closed = False

        def close(self):
            assert not self.closed
            self.closed = True

    connector = TestConnector()
    
    # Call close method once
    connector.close()
    
    # Attempt to call close method again and check for assertion
    with pytest.raises(AssertionError):
        connector.close()

@pytest.mark.asyncio
async def test_close_method_with_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test that close method handles active requests properly."""
    app = web.Application()
    payload = b"test payload"
    
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(1)  # Simulate long request
        return web.Response(body=payload)

    app.router.add_route("GET", "/", handler)
    client = await aiohttp_client(app)

    # Start a request that will take time
    task = asyncio.create_task(client.get("/"))
    
    # Simulate closing the connector while the request is active
    connector = TestConnector()
    connector.close()
    
    # Ensure the request is still running
    await asyncio.sleep(0.5)
    assert not connector.closed  # Should not be closed yet

    # Wait for the request to finish
    response = await task
    await response.read()
    
    # Now the connector should be closed
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_with_no_active_requests(aiohttp_client: AiohttpClient) -> None:
    """Test that close method can be called when there are no active requests."""
    app = web.Application()
    client = await aiohttp_client(app)

    connector = TestConnector()
    
    # No active requests, should close without issues
    connector.close()
    assert connector.closed

@pytest.mark.asyncio
async def test_close_method_state_after_closing(aiohttp_client: AiohttpClient) -> None:
    """Test the state of the connector after closing."""
    app = web.Application()
    client = await aiohttp_client(app)

    connector = TestConnector()
    
    # Close the connector
    connector.close()
    
    # Check the state
    assert connector.closed is True

@pytest.mark.asyncio
async def test_close_method_idempotency(aiohttp_client: AiohttpClient) -> None:
    """Test that calling close multiple times does not raise an error after the first call."""
    app = web.Application()
    client = await aiohttp_client(app)

    connector = TestConnector()
    
    # Call close method once
    connector.close()
    
    # Call close method again, should not raise an error
    connector.close()  # No assertion error should be raised here