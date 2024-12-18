import asyncio
import unittest
from unittest import mock
from aiohttp import TCPConnector

class TestTCPConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

        # Closing again should not raise an error
        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        # Simulate an active connection
        mock_connection = mock.Mock()
        connector._conns = {1: mock_connection}

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)
        self.assertEqual(len(connector._conns), 0)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_cleanup(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector(enable_cleanup_closed=True)
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_without_cleanup(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector(enable_cleanup_closed=False)
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)