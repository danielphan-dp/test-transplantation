import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_connector(self, ClientSessionMock):
        connector = ClientSessionMock.return_value.connector
        self.loop = asyncio.get_event_loop()
        
        # Simulate opening connections
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}
        
        # Close the connector
        self.loop.run_until_complete(connector.close())
        
        # Assert that connections are cleaned up
        self.assertTrue(connector._cleanup_closed_disabled)
        self.assertEqual(len(connector._cleanup_closed_transports), 0)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_active_connections(self, ClientSessionMock):
        connector = ClientSessionMock.return_value.connector
        self.loop = asyncio.get_event_loop()
        
        # Simulate active connections
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}
        connector._cleanup_closed_disabled = False
        
        # Close the connector
        self.loop.run_until_complete(connector.close())
        
        # Assert that connections are still present
        self.assertGreater(len(connector._conns), 0)

    @mock.patch('aiohttp.ClientSession')
    def test_close_no_active_connections(self, ClientSessionMock):
        connector = ClientSessionMock.return_value.connector
        self.loop = asyncio.get_event_loop()
        
        # Simulate no active connections
        connector._conns = {}
        
        # Close the connector
        self.loop.run_until_complete(connector.close())
        
        # Assert that no warnings are raised
        with self.assertRaises(ResourceWarning):
            connector._close_immediately()

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_exception(self, ClientSessionMock):
        connector = ClientSessionMock.return_value.connector
        self.loop = asyncio.get_event_loop()
        
        # Simulate an exception during close
        connector._conns = {1: mock.Mock()}
        connector._close_immediately = mock.Mock(side_effect=ClientConnectionError)
        
        with self.assertRaises(ClientConnectionError):
            self.loop.run_until_complete(connector.close())