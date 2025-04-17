import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout, URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req
        
        async def mock_close():
            req._closed = False
            await req.close()
            req._closed = True

        with mock.patch.object(req, 'close', side_effect=mock_close):
            self.loop.run_until_complete(req.close())
            self.assertTrue(req._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_twice(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req
        
        async def mock_close():
            req._closed = False
            await req.close()
            req._closed = True

        with mock.patch.object(req, 'close', side_effect=mock_close):
            self.loop.run_until_complete(req.close())
            self.assertTrue(req._closed)
            with self.assertRaises(RuntimeError):
                self.loop.run_until_complete(req.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_error(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = req
        
        async def mock_close():
            raise Exception("Close error")

        with mock.patch.object(req, 'close', side_effect=mock_close):
            with self.assertRaises(Exception) as context:
                self.loop.run_until_complete(req.close())
            self.assertEqual(str(context.exception), "Close error")