import asyncio
import unittest
from unittest import mock
from aiohttp import TCPConnector, ClientRequest

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        connector.close()
        self.assertTrue(connector._closed)

        with self.assertRaises(RuntimeError):
            connector.close()  # Ensure it raises an error if closed again

        # Test cleanup behavior
        async def make_conn() -> TCPConnector:
            return connector

        self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        req = ClientRequest("GET", "http://www.python.org", loop=self.loop)

        async def make_conn() -> TCPConnector:
            return connector

        self.loop.run_until_complete(make_conn())
        conn = self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        
        self.assertFalse(connector._closed)
        conn.close()
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)

        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector.close())  # Ensure it raises an error if closed again

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_no_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        connector.close()
        self.assertTrue(connector._closed)