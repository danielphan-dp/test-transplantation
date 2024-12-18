import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectorError

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_connector(self, MockClientSession):
        connector = MockClientSession.return_value.connector
        connector.closed = False
        
        connector.close()
        
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_already_closed_connector(self, MockClientSession):
        connector = MockClientSession.return_value.connector
        connector.closed = True
        
        connector.close()
        
        self.assertTrue(connector.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_active_connections(self, MockClientSession):
        connector = MockClientSession.return_value.connector
        connector.closed = False
        connector._conns = {1: mock.Mock(), 2: mock.Mock()}
        
        connector.close()
        
        self.assertTrue(connector.closed)
        self.assertEqual(len(connector._conns), 0)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_exception_handling(self, MockClientSession):
        connector = MockClientSession.return_value.connector
        connector.closed = False
        connector._conns = {1: mock.Mock()}
        
        with mock.patch.object(connector, '_close_immediately', side_effect=Exception("Close error")):
            with self.assertRaises(Exception):
                connector.close()
        
        self.assertFalse(connector.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_multiple_times(self, MockClientSession):
        connector = MockClientSession.return_value.connector
        connector.closed = False
        
        connector.close()
        connector.close()
        
        self.assertTrue(connector.closed)