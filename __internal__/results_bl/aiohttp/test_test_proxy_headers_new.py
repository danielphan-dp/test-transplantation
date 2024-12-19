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
            loop=asyncio.get_event_loop(),
        )
        
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = asyncio.get_event_loop().run_until_complete(make_conn())
        conn = asyncio.get_event_loop().run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        
        conn.close()
        self.assertIsNone(conn.transport)
        
        # Ensure that calling close multiple times does not raise an error
        try:
            conn.close()
        except Exception as e:
            self.fail(f"close() raised {type(e).__name__} unexpectedly!")

        asyncio.get_event_loop().run_until_complete(connector.close())