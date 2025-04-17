import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession

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
        
        # Assert that the session remains closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    async def test_async_close_session(self, MockClientSession):
        session = MockClientSession()
        session.closed = False
        
        # Call the close method asynchronously
        await session.close()
        
        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    async def test_async_close_already_closed_session(self, MockClientSession):
        session = MockClientSession()
        session.closed = True
        
        # Call the close method asynchronously
        await session.close()
        
        # Assert that the session remains closed
        self.assertTrue(session.closed)

if __name__ == '__main__':
    unittest.main()