import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, ClientConnectorError, ClientTimeout
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False

        # Call the close method
        connector.close()

        # Assert that the connector is marked as closed
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False

        # Call the close method multiple times
        connector.close()
        connector.close()

        # Assert that the connector is still marked as closed
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}

        # Call the close method
        connector.close()

        # Assert that the connections are cleaned up
        self.assertTrue(connector.closed)
        connector._close_immediately.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_no_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        connector._conns = {}

        # Call the close method
        connector.close()

        # Assert that the connector is marked as closed
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_exception_handling(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        connector._conns = {1: mock.Mock()}

        # Simulate an exception during closing
        connector._close_immediately.side_effect = Exception("Close failed")

        with self.assertRaises(Exception):
            connector.close()

        # Assert that the connector is still marked as open
        self.assertFalse(connector.closed)