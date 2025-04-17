import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        req.close = mock.Mock()

        self.assertFalse(req.closed)
        req.close()
        self.assertTrue(req.closed)
        req.close.assert_called_once()

    @mock.patch('aiohttp.client_reqrep.ClientResponse')
    def test_client_response_close(self, ClientResponseMock: mock.Mock) -> None:
        resp = ClientResponse("GET", URL("http://example.com"))
        resp.close = mock.Mock()

        self.assertFalse(resp.closed)
        resp.close()
        self.assertTrue(resp.closed)
        resp.close.assert_called_once()

    @mock.patch('aiohttp.connector.TCPConnector')
    def test_connector_close(self, TCPConnectorMock: mock.Mock) -> None:
        connector = TCPConnector()
        connector.close = mock.Mock()

        self.assertFalse(connector._closed)
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)
        connector.close.assert_called_once()