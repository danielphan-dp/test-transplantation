import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout
from aiohttp.connector import TCPConnector

class TestTCPConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Close the connector
        asyncio.run(connector.close())
        
        # Check if the connector is closed
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        asyncio.run(connector.close())
        
        # Closing again should not raise an error
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        session = ClientSession(connector=connector)
        
        async def make_request():
            async with session.get('http://example.com') as response:
                return await response.text()

        asyncio.run(make_request())
        
        # Close the connector while there are active connections
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_timeout(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        timeout = ClientTimeout(total=0.1)
        session = ClientSession(connector=connector, timeout=timeout)

        async def make_request():
            async with session.get('http://example.com') as response:
                return await response.text()

        asyncio.run(make_request())
        
        # Close the connector with a timeout
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)