import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

class TestClientSessionClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_session(self, MockClientSession):
        session = MockClientSession()
        self.assertIsNone(session.close())
        session.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_with_active_connections(self, MockClientSession):
        session = MockClientSession()
        session._conns = {1: mock.Mock(), 2: mock.Mock()}
        session.close()
        for conn in session._conns.values():
            conn.close.assert_called_once()

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_no_active_connections(self, MockClientSession):
        session = MockClientSession()
        session._conns = {}
        session.close()
        self.assertIsNone(session.close())

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_exception_handling(self, MockClientSession):
        session = MockClientSession()
        session._conns = {1: mock.Mock()}
        session._conns[1].close.side_effect = Exception("Connection error")
        with self.assertRaises(Exception) as context:
            session.close()
        self.assertEqual(str(context.exception), "Connection error")

    @mock.patch('aiohttp.ClientSession')
    def test_close_session_multiple_calls(self, MockClientSession):
        session = MockClientSession()
        session.close()
        session.close()  # Calling close multiple times
        self.assertEqual(session.close.call_count, 1)