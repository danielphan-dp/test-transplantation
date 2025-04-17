import asyncio
import pytest
from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

class TestCloseMethod:
    @pytest.mark.asyncio
    async def test_close_method_not_closed(self, aiohttp_client: AiohttpClient):
        app = web.Application()
        client = await aiohttp_client(app)
        
        # Simulate a connector or resource that has not been closed
        connector = MockConnector()
        assert not connector.closed
        
        connector.close()
        assert connector.closed

    @pytest.mark.asyncio
    async def test_close_method_already_closed(self, aiohttp_client: AiohttpClient):
        app = web.Application()
        client = await aiohttp_client(app)
        
        connector = MockConnector()
        connector.close()  # Close it first
        assert connector.closed
        
        # Attempt to close again and ensure no errors occur
        connector.close()
        assert connector.closed

class MockConnector:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True