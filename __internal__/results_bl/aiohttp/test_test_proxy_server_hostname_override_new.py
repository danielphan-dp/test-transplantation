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

class TestProxyServer(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())
        req.close = AsyncMock()

        self.assertIsNone(req.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_response_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        resp = ClientResponse("GET", URL("http://example.com"), request_info=mock.Mock(), writer=None, continue100=None, timer=TimerNoop(), traces=[], loop=asyncio.get_event_loop(), session=mock.Mock())
        resp.close = AsyncMock()

        self.assertIsNone(resp.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_requests(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = aiohttp.TCPConnector()
        req1 = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())
        req2 = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())

        self.loop.run_until_complete(connector._create_connection(req1, [], aiohttp.ClientTimeout()))
        self.loop.run_until_complete(connector._create_connection(req2, [], aiohttp.ClientTimeout()))

        self.loop.run_until_complete(req1.close())
        self.loop.run_until_complete(req2.close())
        self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = aiohttp.TCPConnector()
        req = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())

        self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))
        self.loop.run_until_complete(req.close())
        self.loop.run_until_complete(connector.close())