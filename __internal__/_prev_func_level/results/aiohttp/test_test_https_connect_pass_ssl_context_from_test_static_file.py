import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close(self, MockClientSession):
        session = MockClientSession()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_awaited_once()

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_multiple_calls(self, MockClientSession):
        session = MockClientSession()
        session.close = mock.AsyncMock()

        async def close_session_twice():
            await session.close()
            await session.close()

        asyncio.run(close_session_twice())
        self.assertEqual(session.close.await_count, 2)

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_with_exception(self, MockClientSession):
        session = MockClientSession()
        session.close = mock.AsyncMock(side_effect=Exception("Close failed"))

        async def close_session_with_exception():
            with self.assertRaises(Exception) as context:
                await session.close()
            self.assertEqual(str(context.exception), "Close failed")

        asyncio.run(close_session_with_exception())

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_no_active_connections(self, MockClientSession):
        session = MockClientSession()
        session.close = mock.AsyncMock()

        async def close_session_no_connections():
            await session.close()

        asyncio.run(close_session_no_connections())
        session.close.assert_awaited_once()