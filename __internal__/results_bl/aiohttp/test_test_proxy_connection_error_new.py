import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from unittest.mock import patch
import pytest
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse, Fingerprint
from aiohttp.connector import _SSL_CONTEXT_VERIFIED
from aiohttp.helpers import TimerNoop
from aiohttp.test_utils import make_mocked_coro

class TestTCPConnectorClose(unittest.TestCase):

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connector(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        # Ensure that the connector is closed properly
        self.assertTrue(connector._closed)

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        self.loop.run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_with_active_connections(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(connector.close())

    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_after_error(self, start_connection: mock.Mock) -> None:
        async def make_conn() -> aiohttp.TCPConnector:
            return aiohttp.TCPConnector()

        connector = self.loop.run_until_complete(make_conn())
        r = {
            "hostname": "www.python.org",
            "host": "127.0.0.1",
            "port": 80,
            "family": socket.AF_INET,
            "proto": 0,
            "flags": socket.AI_NUMERICHOST,
        }
        with mock.patch.object(connector, "_resolve_host", autospec=True, return_value=[r]):
            with mock.patch.object(connector._loop, "create_connection", autospec=True, side_effect=OSError("Connection error")):
                req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
                with self.assertRaises(aiohttp.ClientProxyConnectionError):
                    self.loop.run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
        self.loop.run_until_complete(connector.close())
        self.assertTrue(connector._closed)