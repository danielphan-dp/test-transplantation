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
from aiohttp.helpers import TimerNoop

class TestClientRequestClose(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.python.org"), loop=asyncio.get_event_loop())
        req._closed = False
        
        # Close the request and check if it is marked as closed
        req.close()
        self.assertTrue(req._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_response_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_resp = ClientResponse(
            "get",
            URL("http://proxy.example.com"),
            request_info=mock.Mock(),
            writer=None,
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=asyncio.get_event_loop(),
            session=mock.Mock(),
        )
        proxy_resp._closed = False
        
        # Close the response and check if it is marked as closed
        proxy_resp.close()
        self.assertTrue(proxy_resp._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_double_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.python.org"), loop=asyncio.get_event_loop())
        req.close()
        with self.assertRaises(RuntimeError):
            req.close()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connection(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.python.org"), loop=asyncio.get_event_loop())
        req._closed = False
        req._connection = mock.Mock()
        
        # Simulate an active connection
        req._connection.is_open = True
        
        # Close the request and check if it handles active connection
        req.close()
        self.assertTrue(req._closed)
        self.assertFalse(req._connection.is_open)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_without_connection(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("https://www.python.org"), loop=asyncio.get_event_loop())
        req._connection = None
        
        # Close the request and check if it handles absence of connection
        req.close()
        self.assertTrue(req._closed)