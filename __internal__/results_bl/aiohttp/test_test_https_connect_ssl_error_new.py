import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.helpers import TimerNoop

class TestProxy(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = asyncio.run(make_conn())
        self.assertIsNotNone(connector)

        # Ensure that close can be called multiple times without error
        try:
            connector.close()
            connector.close()  # Calling close again
        except Exception as e:
            self.fail(f"close() raised {type(e).__name__} unexpectedly!")

        # Check if the connector is closed
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = asyncio.run(make_conn())
        self.assertIsNotNone(connector)

        # Simulate an active connection
        connector._active_connections.add(mock.Mock())

        # Close the connector
        connector.close()

        # Check if the active connections are cleared
        self.assertEqual(len(connector._active_connections), 0)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector_with_exception(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = asyncio.run(make_conn())
        self.assertIsNotNone(connector)

        # Simulate an exception during close
        connector._closed = False
        connector._active_connections.add(mock.Mock())
        connector._close = mock.Mock(side_effect=Exception("Close error"))

        with self.assertRaises(Exception):
            connector.close()

        # Ensure that the connector is still marked as not closed
        self.assertFalse(connector._closed)