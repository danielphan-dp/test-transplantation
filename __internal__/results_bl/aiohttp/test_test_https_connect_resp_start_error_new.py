import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from unittest.mock import AsyncMock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.helpers import TimerNoop

class TestClientRequest(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = aiohttp.TCPConnector()
        
        # Ensure the connector is not closed initially
        self.assertFalse(connector._closed)

        # Call the close method
        connector.close()

        # Check if the connector is marked as closed
        self.assertTrue(connector._closed)

        # Ensure that calling close again does not raise an error
        try:
            connector.close()
        except Exception as e:
            self.fail(f"close() raised {type(e).__name__} unexpectedly!")

        # Check if resources are cleaned up
        gc.collect()
        self.assertIsNone(connector._ssl_context)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = aiohttp.TCPConnector()
        
        async def mock_create_connection(*args, **kwargs):
            await asyncio.sleep(0.1)  # Simulate a delay
            return (mock.Mock(), mock.Mock())

        with mock.patch.object(connector, '_create_connection', new_callable=AsyncMock, side_effect=mock_create_connection):
            req = ClientRequest("GET", URL("https://www.python.org"), loop=asyncio.get_event_loop())
            self.loop.run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

            # Call the close method while there are active connections
            connector.close()

            # Check if the connector is marked as closed
            self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_no_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = aiohttp.TCPConnector()
        
        # Call the close method with no active connections
        connector.close()

        # Check if the connector is marked as closed
        self.assertTrue(connector._closed)