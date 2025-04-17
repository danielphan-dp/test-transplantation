import asyncio
import unittest
from unittest import mock
from aiohttp import ClientSession, ClientTimeout, ClientConnectionError

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    def test_close_connector(self, MockClientSession):
        session = MockClientSession()
        connector = session.connector

        # Ensure connector is not closed initially
        self.assertFalse(connector._closed)

        # Close the connector
        asyncio.run(connector.close())

        # Check if the connector is closed
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.ClientSession')
    def test_close_connector_multiple_times(self, MockClientSession):
        session = MockClientSession()
        connector = session.connector

        # Close the connector once
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)

        # Close the connector again and ensure no errors occur
        asyncio.run(connector.close())

    @mock.patch('aiohttp.ClientSession')
    def test_close_connector_with_active_connections(self, MockClientSession):
        session = MockClientSession()
        connector = session.connector

        # Simulate an active connection
        connector._conns = {1: mock.Mock()}

        # Close the connector
        asyncio.run(connector.close())

        # Ensure all connections are cleaned up
        self.assertTrue(connector._closed)
        self.assertEqual(len(connector._conns), 0)

    @mock.patch('aiohttp.ClientSession')
    def test_close_connector_with_exception(self, MockClientSession):
        session = MockClientSession()
        connector = session.connector

        # Simulate an exception during close
        connector._close_immediately = mock.Mock(side_effect=ClientConnectionError)

        with self.assertRaises(ClientConnectionError):
            asyncio.run(connector.close())

        # Ensure the connector is still marked as closed
        self.assertTrue(connector._closed)