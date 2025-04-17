import asyncio
import unittest
from unittest import mock
import aiohttp
from aiohttp import ClientRequest, ClientResponse
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    @mock.patch('aiohttp.client_reqrep.ClientRequest')
    @mock.patch('aiohttp.connector.start_connection', autospec=True, spec_set=True)
    def test_close_method(self, start_connection, ClientRequestMock):
        req = ClientRequest("GET", URL("http://example.com"), loop=self.loop)
        ClientRequestMock.return_value = req

        with mock.patch.object(req, 'close', autospec=True) as mock_close:
            self.loop.run_until_complete(req.close())
            mock_close.assert_called_once()

        # Test closing an already closed request
        with mock.patch.object(req, 'close', autospec=True) as mock_close:
            self.loop.run_until_complete(req.close())
            mock_close.assert_called_once()

        # Test if close method handles exceptions
        with mock.patch.object(req, 'close', side_effect=Exception("Close failed")):
            with self.assertRaises(Exception):
                self.loop.run_until_complete(req.close())

    @mock.patch('aiohttp.client_reqrep.ClientResponse')
    def test_client_response_close(self, ClientResponseMock):
        resp = ClientResponse("GET", URL("http://example.com"), request_info=mock.Mock(), loop=self.loop)
        ClientResponseMock.return_value = resp

        with mock.patch.object(resp, 'close', autospec=True) as mock_close:
            self.loop.run_until_complete(resp.close())
            mock_close.assert_called_once()

        # Test closing an already closed response
        with mock.patch.object(resp, 'close', autospec=True) as mock_close:
            self.loop.run_until_complete(resp.close())
            mock_close.assert_called_once()

        # Test if close method handles exceptions
        with mock.patch.object(resp, 'close', side_effect=Exception("Close failed")):
            with self.assertRaises(Exception):
                self.loop.run_until_complete(resp.close())

if __name__ == '__main__':
    unittest.main()