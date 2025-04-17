import asyncio
import gc
import socket
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.helpers import TimerNoop

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        ClientRequestMock.return_value = req

        async def close_request():
            await req.close()

        self.assertFalse(req.closed)
        asyncio.run(close_request())
        self.assertTrue(req.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        ClientRequestMock.return_value = req

        async def close_request():
            await req.close()
            await req.close()  # Closing again should not raise an error

        asyncio.run(close_request())
        self.assertTrue(req.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )
        response = ClientResponse(
            "GET",
            URL("http://example.com"),
            request_info=mock.Mock(),
            writer=None,
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=asyncio.get_event_loop(),
            session=mock.Mock(),
        )
        req._response = response

        async def close_request():
            await req.close()

        asyncio.run(close_request())
        self.assertTrue(req.closed)
        self.assertTrue(response.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_without_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest(
            "GET",
            URL("http://example.com"),
            loop=asyncio.get_event_loop(),
        )

        async def close_request():
            await req.close()

        asyncio.run(close_request())
        self.assertTrue(req.closed)