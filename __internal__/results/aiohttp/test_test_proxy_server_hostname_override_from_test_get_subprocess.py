import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout

class TestConnectorClose(unittest.TestCase):
    
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        
        async def close_connector():
            await connector.close()
        
        self.loop.run_until_complete(close_connector())
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_already_closed_connector(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = True
        
        async def close_connector():
            await connector.close()
        
        self.loop.run_until_complete(close_connector())
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}
        
        async def close_connector():
            await connector.close()
        
        self.loop.run_until_complete(close_connector())
        self.assertTrue(connector.closed)
        self.assertEqual(len(connector._conns), 0)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_cleanup(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = mock.Mock()
        connector.closed = False
        connector._cleanup_closed = mock.Mock()
        
        async def close_connector():
            await connector.close()
        
        self.loop.run_until_complete(close_connector())
        connector._cleanup_closed.assert_called_once()
        self.assertTrue(connector.closed)