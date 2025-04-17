import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_with_active_requests(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()
        session._active_requests = [mock.Mock(), mock.Mock()]

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_no_active_requests(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()
        session._active_requests = []

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_exception_handling(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock(side_effect=Exception("Close failed"))

        async def close_session():
            try:
                await session.close()
            except Exception as e:
                return str(e)

        result = asyncio.run(close_session())
        self.assertEqual(result, "Close failed")

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_multiple_calls(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()
            await session.close()

        asyncio.run(close_session())
        self.assertEqual(session.close.call_count, 1)