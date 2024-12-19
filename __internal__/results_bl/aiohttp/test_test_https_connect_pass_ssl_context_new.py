import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from unittest.mock import AsyncMock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.connector import _SSL_CONTEXT_VERIFIED
from aiohttp.helpers import TimerNoop

class TestClientRequestClose(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.example.com"), loop=asyncio.get_event_loop())
        req.close = AsyncMock()

        self.assertIsNone(req.close())
        req.close.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_multiple_calls(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.example.com"), loop=asyncio.get_event_loop())
        req.close = AsyncMock()

        for _ in range(3):
            self.loop.run_until_complete(req.close())

        self.assertEqual(req.close.call_count, 3)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_exception(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.example.com"), loop=asyncio.get_event_loop())
        req.close = AsyncMock(side_effect=Exception("Close failed"))

        with self.assertRaises(Exception) as context:
            self.loop.run_until_complete(req.close())
        
        self.assertEqual(str(context.exception), "Close failed")

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_no_active_connection(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.example.com"), loop=asyncio.get_event_loop())
        req.close = AsyncMock()

        self.loop.run_until_complete(req.close())
        self.assertIsNone(req.close())
        req.close.assert_called_once()