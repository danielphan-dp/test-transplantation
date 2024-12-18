import asyncio
import gc
import socket
import ssl
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_connection(self, start_connection, ClientRequestMock):
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            proxy=URL("http://proxy.example.com"),
            loop=asyncio.get_event_loop(),
        )
        
        async def make_conn():
            return aiohttp.TCPConnector()

        connector = asyncio.get_event_loop().run_until_complete(make_conn())
        proto = mock.Mock()
        conn = mock.Mock()
        conn._protocol = proto
        conn.transport = proto.transport
        
        with mock.patch.object(connector, 'connect', return_value=conn):
            connection = asyncio.get_event_loop().run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
            connection.close()
            self.assertIsNone(connection._protocol)
            self.assertIsNone(connection.transport)

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_multiple_times(self, start_connection, ClientRequestMock):
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            proxy=URL("http://proxy.example.com"),
            loop=asyncio.get_event_loop(),
        )
        
        async def make_conn():
            return aiohttp.TCPConnector()

        connector = asyncio.get_event_loop().run_until_complete(make_conn())
        proto = mock.Mock()
        conn = mock.Mock()
        conn._protocol = proto
        conn.transport = proto.transport
        
        with mock.patch.object(connector, 'connect', return_value=conn):
            connection = asyncio.get_event_loop().run_until_complete(connector.connect(req, [], aiohttp.ClientTimeout()))
            connection.close()
            with self.assertRaises(Exception):
                connection.close()

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_without_connect(self, start_connection, ClientRequestMock):
        req = ClientRequest(
            "GET",
            URL("http://www.python.org"),
            proxy=URL("http://proxy.example.com"),
            loop=asyncio.get_event_loop(),
        )
        
        async def make_conn():
            return aiohttp.TCPConnector()

        connector = asyncio.get_event_loop().run_until_complete(make_conn())
        
        with self.assertRaises(AttributeError):
            conn = mock.Mock()
            conn.close()