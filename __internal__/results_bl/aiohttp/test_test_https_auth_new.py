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
    def test_close_method(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        ClientRequestMock.return_value = req

        self.assertIsNone(req.close())
        self.assertTrue(req._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method_multiple_calls(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        ClientRequestMock.return_value = req

        req.close()
        with self.assertRaises(RuntimeError):
            req.close()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method_with_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_resp = ClientResponse(
            "get",
            URL("http://example.com"),
            request_info=mock.Mock(),
            writer=None,
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=asyncio.get_event_loop(),
            session=mock.Mock(),
        )
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        req._response = proxy_resp

        req.close()
        self.assertTrue(req._closed)
        self.assertTrue(proxy_resp._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method_no_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )

        req.close()
        self.assertTrue(req._closed)
        self.assertIsNone(req._response)