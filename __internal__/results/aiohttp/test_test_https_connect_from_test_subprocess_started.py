import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout, URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req

        self.assertFalse(req.closed)
        asyncio.run(req.close())
        self.assertTrue(req.closed)

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req

        asyncio.run(req.close())
        with self.assertRaises(RuntimeError):
            asyncio.run(req.close())

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        response = ClientResponse("GET", URL("http://example.com"), request_info=mock.Mock(), writer=None, loop=asyncio.get_event_loop())
        ClientRequestMock.return_value = req

        asyncio.run(req.close())
        self.assertTrue(req.closed)
        self.assertIsNone(response._response)

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_no_response(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req

        asyncio.run(req.close())
        self.assertTrue(req.closed)