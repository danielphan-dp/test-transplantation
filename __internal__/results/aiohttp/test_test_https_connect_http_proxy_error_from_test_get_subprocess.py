import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        
        # Call the close method
        session.close()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_already_closed_session(self, MockClientSession):
        session = MockClientSession()
        session.closed = True
        
        # Call the close method
        session.close()
        
        # Assert that calling close on an already closed session does not change the state
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_active_connections(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        session._conns = {1: mock.Mock(), 2: mock.Mock()}  # Simulate active connections
        
        # Call the close method
        session.close()
        
        # Assert that connections are closed
        for conn in session._conns.values():
            conn.close.assert_called_once()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_no_active_connections(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        session._conns = {}  # No active connections
        
        # Call the close method
        session.close()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_exception_handling(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        session._conns = {1: mock.Mock()}
        
        # Simulate an exception during connection close
        session._conns[1].close.side_effect = Exception("Connection close error")
        
        # Call the close method
        with self.assertRaises(Exception):
            session.close()
        
        # Assert that the session is still marked as closed
        self.assertTrue(session.closed)