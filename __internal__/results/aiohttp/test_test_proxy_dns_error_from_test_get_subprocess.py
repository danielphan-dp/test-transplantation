import asyncio
import unittest
from unittest import mock
import aiohttp
from aiohttp import ClientRequest
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.assertFalse(connector._closed)

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_exception(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        with mock.patch.object(connector, "_cleanup_closed", side_effect=Exception("Test Exception")):
            with self.assertRaises(Exception):
                self.loop.run_until_complete(connector.close())