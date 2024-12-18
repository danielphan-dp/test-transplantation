import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_close_connector(self, MockTCPConnector, MockClientRequest):
        connector = MockTCPConnector()
        connector.closed = False

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_close_already_closed_connector(self, MockTCPConnector, MockClientRequest):
        connector = MockTCPConnector()
        connector.closed = True

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_close_with_active_connections(self, MockTCPConnector, MockClientRequest):
        connector = MockTCPConnector()
        connector.closed = False
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}

        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector.closed)
        self.assertEqual(len(connector._conns), 0)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.TCPConnector')
    def test_close_with_cleanup(self, MockTCPConnector, MockClientRequest):
        connector = MockTCPConnector()
        connector.closed = False
        connector._cleanup_closed = mock.Mock()

        self.loop.run_until_complete(connector.close())
        connector._cleanup_closed.assert_called_once()
        self.assertTrue(connector.closed)