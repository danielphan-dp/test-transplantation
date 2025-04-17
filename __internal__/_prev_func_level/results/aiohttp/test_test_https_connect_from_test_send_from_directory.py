import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        req.close = mock.AsyncMock()

        self.loop.run_until_complete(req.close())
        req.close.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        req.close = mock.AsyncMock()

        self.loop.run_until_complete(req.close())
        self.loop.run_until_complete(req.close())
        self.assertEqual(req.close.call_count, 2)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_resp = ClientResponse("get", URL("http://example.com"), request_info=mock.Mock(), writer=None, continue100=None, timer=mock.Mock(), traces=[], loop=self.loop, session=mock.Mock())
        req = ClientRequest("GET", URL("http://example.com"))
        req.close = mock.AsyncMock()

        self.loop.run_until_complete(req.close())
        proxy_resp.close()
        req.close.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_error(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        req.close = mock.AsyncMock(side_effect=Exception("Close error"))

        with self.assertRaises(Exception):
            self.loop.run_until_complete(req.close())
        req.close.assert_called_once()