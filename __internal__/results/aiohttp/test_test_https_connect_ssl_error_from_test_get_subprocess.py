import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, ClientConnectorError, TCPConnector
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Close the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

        # Ensure that calling close again does not raise an error
        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Simulate an active connection
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        connector._conns[req] = mock.Mock()

        # Close the connector
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

        # Ensure that the active connection is cleaned up
        self.assertNotIn(req, connector._conns)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_exception(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Simulate an exception during close
        with mock.patch.object(connector, '_cleanup_closed', side_effect=Exception("Cleanup failed")):
            with self.assertRaises(Exception):
                self.loop.run_until_complete(connector.close())

        self.assertFalse(connector._closed)  # Ensure the connector is still open

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Close the connector multiple times
        for _ in range(3):
            self.loop.run_until_complete(connector.close())

        self.assertTrue(connector._closed)