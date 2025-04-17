import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

class TestConnectorClose:
    async def test_close_connector_not_closed(self, aiohttp_client: AiohttpClient) -> None:
        """Test that close method marks the connector as closed."""
        app = web.Application()
        client = await aiohttp_client(app)
        assert not client.closed
        client.close()
        assert client.closed

    async def test_close_connector_already_closed(self, aiohttp_client: AiohttpClient) -> None:
        """Test that calling close on an already closed connector does not raise an error."""
        app = web.Application()
        client = await aiohttp_client(app)
        client.close()
        client.close()  # Should not raise an error

    async def test_close_connector_with_active_requests(self, aiohttp_client: AiohttpClient) -> None:
        """Test that close method can be called while there are active requests."""
        app = web.Application()
        payload = b"test"
        
        async def handler(request: web.Request) -> web.Response:
            return web.Response(body=payload)

        app.router.add_route("GET", "/", handler)
        client = await aiohttp_client(app)

        async def make_request():
            await client.get("/")

        await asyncio.gather(make_request(), make_request())
        client.close()
        assert client.closed

    async def test_close_connector_with_pending_tasks(self, aiohttp_client: AiohttpClient) -> None:
        """Test that close method handles pending tasks gracefully."""
        app = web.Application()
        client = await aiohttp_client(app)

        async def pending_task():
            await asyncio.sleep(1)

        task = asyncio.create_task(pending_task())
        client.close()
        await asyncio.sleep(0.1)  # Allow some time for close to be processed
        assert client.closed
        await task  # Ensure the task completes without issues

    async def test_close_connector_multiple_times(self, aiohttp_client: AiohttpClient) -> None:
        """Test that closing the connector multiple times does not cause issues."""
        app = web.Application()
        client = await aiohttp_client(app)
        client.close()
        client.close()  # Should not raise an error
        assert client.closed