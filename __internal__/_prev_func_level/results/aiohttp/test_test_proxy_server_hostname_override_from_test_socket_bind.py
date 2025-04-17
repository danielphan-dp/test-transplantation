import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        self.assertFalse(connector._closed)
        
        # Simulate closing the connector
        asyncio.run(connector.close())
        
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)
        
        # Closing again should not raise an error
        asyncio.run(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        
        # Simulate an active connection
        req = ClientRequest("GET", URL("http://example.com"), connector=connector)
        asyncio.run(connector._create_connection(req, [], ClientTimeout()))
        
        self.assertFalse(connector._closed)
        
        # Close the connector
        asyncio.run(connector.close())
        
        self.assertTrue(connector._closed)