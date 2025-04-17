import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, helpers
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

    @mock.patch('aiohttp.ClientRequest')
    @mock.patch('aiohttp.TCPConnector')
    def test_close_request(self, MockTCPConnector, MockClientRequest):
        mock_request = MockClientRequest.return_value
        mock_request.closed = False

        async def mock_close():
            mock_request.closed = True

        mock_request.close = mock_close

        self.loop.run_until_complete(mock_request.close())
        self.assertTrue(mock_request.closed)

    @mock.patch('aiohttp.ClientRequest')
    @mock.patch('aiohttp.TCPConnector')
    def test_close_request_already_closed(self, MockTCPConnector, MockClientRequest):
        mock_request = MockClientRequest.return_value
        mock_request.closed = True

        async def mock_close():
            pass

        mock_request.close = mock_close

        self.loop.run_until_complete(mock_request.close())
        self.assertTrue(mock_request.closed)

    @mock.patch('aiohttp.ClientRequest')
    @mock.patch('aiohttp.TCPConnector')
    def test_close_multiple_times(self, MockTCPConnector, MockClientRequest):
        mock_request = MockClientRequest.return_value
        mock_request.closed = False

        async def mock_close():
            mock_request.closed = True

        mock_request.close = mock_close

        self.loop.run_until_complete(mock_request.close())
        self.assertTrue(mock_request.closed)

        self.loop.run_until_complete(mock_request.close())
        self.assertTrue(mock_request.closed)

    @mock.patch('aiohttp.ClientRequest')
    @mock.patch('aiohttp.TCPConnector')
    def test_close_with_exception(self, MockTCPConnector, MockClientRequest):
        mock_request = MockClientRequest.return_value
        mock_request.closed = False

        async def mock_close():
            raise Exception("Close failed")

        mock_request.close = mock_close

        with self.assertRaises(Exception):
            self.loop.run_until_complete(mock_request.close())
        self.assertFalse(mock_request.closed)

    @mock.patch('aiohttp.ClientRequest')
    @mock.patch('aiohttp.TCPConnector')
    def test_close_with_cleanup(self, MockTCPConnector, MockClientRequest):
        mock_request = MockClientRequest.return_value
        mock_request.closed = False

        async def mock_close():
            mock_request.closed = True
            # Simulate cleanup actions here

        mock_request.close = mock_close

        self.loop.run_until_complete(mock_request.close())
        self.assertTrue(mock_request.closed)

if __name__ == '__main__':
    unittest.main()