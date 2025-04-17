import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        
        # Call the close method
        session.close()
        
        # Assert that the session is now closed
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
        session._conns = mock.Mock()  # Simulate active connections
        
        # Call the close method
        session.close()
        
        # Assert that the connections are cleaned up
        session._conns.clear.assert_called_once()
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_exception_handling(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        
        # Simulate an exception during close
        session._cleanup_closed = mock.Mock(side_effect=Exception("Cleanup failed"))
        
        with self.assertRaises(Exception):
            session.close()
        
        # Assert that the session is still closed
        self.assertTrue(session.closed)

if __name__ == '__main__':
    unittest.main()