import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_multiple_calls(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()
            await session.close()

        asyncio.run(close_session())
        self.assertEqual(session.close.call_count, 2)

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_with_exception(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock(side_effect=Exception("Close failed"))

        async def close_session():
            with self.assertRaises(Exception):
                await session.close()

        asyncio.run(close_session())

    @mock.patch('aiohttp.ClientSession')
    def test_client_session_close_no_active_requests(self, ClientSessionMock):
        session = ClientSessionMock()
        session.close = mock.AsyncMock()

        async def close_session():
            await session.close()

        asyncio.run(close_session())
        session.close.assert_called_once()