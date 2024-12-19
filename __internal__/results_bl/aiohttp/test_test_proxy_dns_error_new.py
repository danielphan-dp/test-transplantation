import asyncio
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest

class TestProxy(unittest.TestCase):

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        # Ensure that closing the connector does not raise any exceptions
        self.assertIsNone(connector._closed)

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        # Closing again should not raise an error
        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            loop=self.loop,
        )
        self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        # Closing the connector while there are active connections
        self.loop.run_until_complete(connector.close())
        # Ensure that the connector is closed
        self.assertTrue(connector._closed)