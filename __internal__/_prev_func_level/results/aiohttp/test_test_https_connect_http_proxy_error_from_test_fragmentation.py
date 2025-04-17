import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, MockClientSession):
        session = MockClientSession()
        loop = asyncio.get_event_loop()
        
        async def close_session():
            await session.close()

        loop.run_until_complete(close_session())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_with_active_connections(self, MockClientSession):
        session = MockClientSession()
        session._conns = {1: mock.Mock(), 2: mock.Mock()}
        loop = asyncio.get_event_loop()

        async def close_session():
            await session.close()

        loop.run_until_complete(close_session())
        for conn in session._conns.values():
            conn.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_error_handling(self, MockClientSession):
        session = MockClientSession()
        session.close.side_effect = ClientConnectionError("Connection error")
        loop = asyncio.get_event_loop()

        async def close_session():
            with self.assertRaises(ClientConnectionError):
                await session.close()

        loop.run_until_complete(close_session())

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_multiple_calls(self, MockClientSession):
        session = MockClientSession()
        loop = asyncio.get_event_loop()

        async def close_session():
            await session.close()
            await session.close()  # Call close again

        loop.run_until_complete(close_session())
        session.close.assert_called_once()  # Ensure close is only called once

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_with_timeout(self, MockClientSession):
        session = MockClientSession()
        loop = asyncio.get_event_loop()

        async def close_session():
            timeout = ClientTimeout(total=1)
            await session.close(timeout=timeout)

        loop.run_until_complete(close_session())
        session.close.assert_called_once()  # Ensure close is called with timeout

if __name__ == '__main__':
    unittest.main()