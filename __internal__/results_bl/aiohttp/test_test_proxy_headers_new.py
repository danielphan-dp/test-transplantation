import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse

class TestClientRequestClose(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            loop=self.loop,
        )
        
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        conn = self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        
        # Ensure close method can be called without error
        conn.close()
        
        # Check if the connection is closed
        with self.assertRaises(RuntimeError):
            conn._protocol.transport

        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            loop=self.loop,
        )
        
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        conn = self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        
        # Close the connection multiple times
        conn.close()
        conn.close()  # Should not raise an error
        
        self.loop.run_until_complete(connector.close())