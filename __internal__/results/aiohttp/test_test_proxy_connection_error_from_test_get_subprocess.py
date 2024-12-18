import asyncio
import unittest
from unittest import mock
import aiohttp
from aiohttp import ClientRequest
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.connector = aiohttp.TCPConnector()

    def tearDown(self):
        self.loop.run_until_complete(self.connector.close())

    def test_close_connector(self):
        self.assertFalse(self.connector._closed)
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    def test_close_multiple_times(self):
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)
        self.loop.run_until_complete(self.connector.close())  # Should not raise an error

    def test_close_with_active_connections(self):
        async def make_request():
            req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
            return await self.connector.connect(req, [], aiohttp.ClientTimeout())

        self.loop.run_until_complete(make_request())
        self.assertFalse(self.connector._closed)
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    def test_close_with_exception(self):
        with mock.patch.object(self.connector, "_cleanup_closed", side_effect=Exception("Cleanup failed")):
            with self.assertRaises(Exception):
                self.loop.run_until_complete(self.connector.close())

    def test_close_no_active_connections(self):
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

if __name__ == '__main__':
    unittest.main()