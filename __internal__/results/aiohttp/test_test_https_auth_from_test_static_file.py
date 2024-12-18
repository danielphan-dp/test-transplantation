import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, helpers
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        ClientRequestMock.return_value = req

        with mock.patch.object(req, 'close', autospec=True) as mock_close:
            self.loop.run_until_complete(req.close())
            mock_close.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_client_response_close(self, start_connection, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        resp = ClientResponse("GET", URL("http://example.com"), request_info=mock.Mock(), writer=None, loop=self.loop)
        
        with mock.patch.object(resp, 'close', autospec=True) as mock_resp_close:
            self.loop.run_until_complete(resp.close())
            mock_resp_close.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_requests(self, start_connection, ClientRequestMock):
        req1 = ClientRequest("GET", URL("http://example.com/1"), loop=self.loop)
        req2 = ClientRequest("GET", URL("http://example.com/2"), loop=self.loop)

        with mock.patch.object(req1, 'close', autospec=True) as mock_close1, \
             mock.patch.object(req2, 'close', autospec=True) as mock_close2:
            self.loop.run_until_complete(req1.close())
            self.loop.run_until_complete(req2.close())
            mock_close1.assert_called_once()
            mock_close2.assert_called_once()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_close_with_exception(self, start_connection, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)

        with mock.patch.object(req, 'close', side_effect=Exception("Close failed")) as mock_close:
            with self.assertRaises(Exception) as context:
                self.loop.run_until_complete(req.close())
            self.assertEqual(str(context.exception), "Close failed")
            mock_close.assert_called_once()

    def tearDown(self):
        pass