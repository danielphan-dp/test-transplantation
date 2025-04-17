import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout

class TestClientSessionClose(unittest.TestCase):
    
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = False
        
        # Call the close method
        session.close()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_already_closed_session(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = True
        
        # Call the close method
        session.close()
        
        # Assert that calling close on an already closed session does not change the state
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    async def test_async_close_session(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = False
        
        # Simulate an async close
        await session.close()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    async def test_async_close_already_closed_session(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = True
        
        # Simulate an async close
        await session.close()
        
        # Assert that calling close on an already closed session does not change the state
        self.assertTrue(session.closed)

if __name__ == '__main__':
    unittest.main()