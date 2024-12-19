import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from unittest.mock import AsyncMock
import pytest
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse

class TestClientRequestClose(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connection(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_req = ClientRequest("GET", URL("http://proxy.example.com"), loop=self.loop)
        ClientRequestMock.return_value = proxy_req

        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://localhost:1234/path"), loop=self.loop)
        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

        # Close the connector and check if it cleans up resources
        self.loop.run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_req = ClientRequest("GET", URL("http://proxy.example.com"), loop=self.loop)
        ClientRequestMock.return_value = proxy_req

        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://localhost:1234/path"), loop=self.loop)
        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

        # Close the connector multiple times
        self.loop.run_until_complete(connector.close())
        self.loop.run_until_complete(connector.close())  # Should not raise an error

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_requests(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_req = ClientRequest("GET", URL("http://proxy.example.com"), loop=self.loop)
        ClientRequestMock.return_value = proxy_req

        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://localhost:1234/path"), loop=self.loop)
        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

        # Attempt to close while there are active requests
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector.close())  # Should raise an error due to active requests

        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))
        self.loop.run_until_complete(connector.close())  # Now it should close without error

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.run_until_complete(gc.collect())
        self.loop.close()