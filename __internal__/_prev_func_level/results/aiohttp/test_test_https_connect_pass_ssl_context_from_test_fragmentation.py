import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_client_request_close(self, MockTCPConnector, MockClientRequest):
        loop = asyncio.get_event_loop()
        req = MockClientRequest("GET", URL("http://example.com"), loop=loop)
        req.close = mock.AsyncMock()

        connector = MockTCPConnector()
        connector.close = mock.AsyncMock()

        loop.run_until_complete(req.close())
        req.close.assert_called_once()
        loop.run_until_complete(connector.close())
        connector.close.assert_called_once()

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_client_request_close_multiple_calls(self, MockTCPConnector, MockClientRequest):
        loop = asyncio.get_event_loop()
        req = MockClientRequest("GET", URL("http://example.com"), loop=loop)
        req.close = mock.AsyncMock()

        for _ in range(3):
            loop.run_until_complete(req.close())

        self.assertEqual(req.close.call_count, 3)

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_client_request_close_with_exception(self, MockTCPConnector, MockClientRequest):
        loop = asyncio.get_event_loop()
        req = MockClientRequest("GET", URL("http://example.com"), loop=loop)
        req.close = mock.AsyncMock(side_effect=Exception("Close failed"))

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(req.close())
        self.assertEqual(str(context.exception), "Close failed")

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_connector_close(self, MockTCPConnector, MockClientRequest):
        loop = asyncio.get_event_loop()
        connector = MockTCPConnector()
        connector.close = mock.AsyncMock()

        loop.run_until_complete(connector.close())
        connector.close.assert_called_once()