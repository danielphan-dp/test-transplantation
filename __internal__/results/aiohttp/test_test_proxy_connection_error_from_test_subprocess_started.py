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

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock):
        self.loop.run_until_complete(self.connector.connect(ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)))
        self.assertFalse(self.connector._closed)
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock):
        self.loop.run_until_complete(self.connector.connect(ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)))
        self.loop.run_until_complete(self.connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(self.connector.close())

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock):
        req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        self.loop.run_until_complete(self.connector.connect(req))
        self.loop.run_until_complete(self.connector.close())
        self.assertTrue(self.connector._closed)

    def tearDown(self):
        self.loop.run_until_complete(self.connector.close())