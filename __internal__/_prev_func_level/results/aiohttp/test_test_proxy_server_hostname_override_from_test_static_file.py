import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientResponse, TCPConnector

class TestConnectorClose(unittest.TestCase):
    
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        async def make_request():
            async with ClientSession(connector=connector) as session:
                async with session.get('http://example.com') as response:
                    return response
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(make_request())
        
        self.assertFalse(connector._closed)
        
        loop.run_until_complete(connector.close())
        
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        async def make_request():
            async with ClientSession(connector=connector) as session:
                async with session.get('http://example.com') as response:
                    return response
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(make_request())
        
        loop.run_until_complete(connector.close())
        
        with self.assertRaises(RuntimeError):
            loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close_with_active_requests(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        async def make_request():
            async with ClientSession(connector=connector) as session:
                await session.get('http://example.com')
        
        loop = asyncio.get_event_loop()
        task = loop.create_task(make_request())
        
        loop.run_until_complete(asyncio.sleep(0.1))  # Allow the request to start
        
        with self.assertRaises(RuntimeError):
            loop.run_until_complete(connector.close())
        
        loop.run_until_complete(task)  # Ensure the request completes
        loop.run_until_complete(connector.close())  # Now close should succeed