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

        # Assert that the session remains closed
        self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_active_requests(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = False

        # Simulate an active request
        async def mock_request():
            await asyncio.sleep(0.1)

        with mock.patch.object(session, 'get', side_effect=mock_request):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(session.get('http://example.com'))

            # Call the close method
            session.close()

            # Assert that the session is marked as closed
            self.assertTrue(session.closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_with_timeout(self, ClientSessionMock):
        session = ClientSessionMock()
        session.closed = False

        # Call the close method with a timeout
        timeout = ClientTimeout(total=0.1)
        session.close()

        # Assert that the session is marked as closed
        self.assertTrue(session.closed)

if __name__ == '__main__':
    unittest.main()