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

        connector = self.loop.run_until_complete(make_conn())
        self.assertIsNotNone(connector)

        # Close the connector and check if it is closed
        self.loop.run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector._create_connection(mock.Mock(), [], aiohttp.ClientTimeout()))

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        self.loop.run_until_complete(connector.close())  # Closing again should not raise an error

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

        # Close the connector while there are active connections
        self.loop.run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))