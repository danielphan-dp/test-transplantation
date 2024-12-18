import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, helpers
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())
        ClientRequestMock.return_value = req
        
        # Simulate sending a request
        resp = ClientResponse("get", URL("http://example.com"), request_info=mock.Mock(), writer=None, continue100=None, timer=helpers.TimerNoop(), traces=[], loop=asyncio.get_event_loop(), session=mock.Mock())
        with mock.patch.object(req, "send", autospec=True, return_value=resp):
            self.assertFalse(req.closed)
            asyncio.get_event_loop().run_until_complete(req.close())
            self.assertTrue(req.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())
        ClientRequestMock.return_value = req
        
        # Simulate sending a request
        resp = ClientResponse("get", URL("http://example.com"), request_info=mock.Mock(), writer=None, continue100=None, timer=helpers.TimerNoop(), traces=[], loop=asyncio.get_event_loop(), session=mock.Mock())
        with mock.patch.object(req, "send", autospec=True, return_value=resp):
            asyncio.get_event_loop().run_until_complete(req.close())
            self.assertTrue(req.closed)
            with self.assertRaises(RuntimeError):
                asyncio.get_event_loop().run_until_complete(req.close())

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close_with_error(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        req = ClientRequest("GET", URL("http://example.com"), loop=asyncio.get_event_loop())
        ClientRequestMock.return_value = req
        
        # Simulate sending a request
        resp = ClientResponse("get", URL("http://example.com"), request_info=mock.Mock(), writer=None, continue100=None, timer=helpers.TimerNoop(), traces=[], loop=asyncio.get_event_loop(), session=mock.Mock())
        with mock.patch.object(req, "send", autospec=True, return_value=resp):
            asyncio.get_event_loop().run_until_complete(req.close())
            self.assertTrue(req.closed)
            with self.assertRaises(RuntimeError):
                asyncio.get_event_loop().run_until_complete(req.close())  # Attempt to close again should raise an error

if __name__ == '__main__':
    unittest.main()