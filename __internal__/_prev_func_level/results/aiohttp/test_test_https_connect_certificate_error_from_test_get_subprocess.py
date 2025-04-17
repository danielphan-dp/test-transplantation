import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, ClientConnectorError, ClientTimeout
from yarl import URL
from aiohttp.connector import TCPConnector

class TestTCPConnectorClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.connector = TCPConnector()

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_connector(self, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        ClientRequestMock.return_value = req

        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_connector_multiple_times(self, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        ClientRequestMock.return_value = req

        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(self.connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_with_active_connections(self, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        ClientRequestMock.return_value = req

        async def make_connection():
            await self.connector._create_connection(req, [], ClientTimeout())

        self.loop.run_until_complete(make_connection())
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    def tearDown(self):
        self.loop.run_until_complete(self.connector.close())