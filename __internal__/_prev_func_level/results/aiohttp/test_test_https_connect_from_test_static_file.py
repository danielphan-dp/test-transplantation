import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, ClientSessionMock):
        session = ClientSessionMock()
        self.assertFalse(session.closed)

        asyncio.run(session.close())
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_multiple_times(self, ClientSessionMock):
        session = ClientSessionMock()
        asyncio.run(session.close())
        self.assertTrue(session.closed)

        with self.assertRaises(RuntimeError):
            asyncio.run(session.close())

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_active_requests(self, ClientSessionMock):
        session = ClientSessionMock()
        session._connector = mock.Mock()
        session._connector.close = mock.AsyncMock()

        async def mock_request():
            await asyncio.sleep(0.1)

        task = asyncio.create_task(mock_request())
        asyncio.run(session.close())
        self.assertTrue(session.closed)
        self.assertTrue(session._connector.close.called)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_timeout(self, ClientSessionMock):
        session = ClientSessionMock()
        session._connector = mock.Mock()
        session._connector.close = mock.AsyncMock()

        timeout = ClientTimeout(total=0.1)
        session.timeout = timeout

        async def mock_request():
            await asyncio.sleep(0.2)

        task = asyncio.create_task(mock_request())
        with self.assertRaises(asyncio.TimeoutError):
            asyncio.run(session.close())
        self.assertTrue(session.closed)
        self.assertTrue(session._connector.close.called)