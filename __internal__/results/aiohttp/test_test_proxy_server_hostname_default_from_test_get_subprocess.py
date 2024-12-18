import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout, web
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Simulate closing the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

        # Ensure that closing again does not raise an error
        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        req = ClientRequest("GET", URL("http://example.com"), connector=connector)

        # Simulate an active connection
        self.loop.run_until_complete(req.send())
        self.assertFalse(connector._closed)

        # Close the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_unclosed_requests(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        req1 = ClientRequest("GET", URL("http://example.com"), connector=connector)
        req2 = ClientRequest("GET", URL("http://example.org"), connector=connector)

        # Simulate sending requests
        self.loop.run_until_complete(req1.send())
        self.loop.run_until_complete(req2.send())
        
        # Close the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_cleanup(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._cleanup_closed)

        # Close the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._cleanup_closed)