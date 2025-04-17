import asyncio
import unittest
from unittest import mock
from aiohttp import TCPConnector, ClientRequest, ClientResponse
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.connector = TCPConnector()

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_connector(self, ClientRequestMock):
        req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        conn = self.loop.run_until_complete(self.connector.connect(req, [], None))
        
        self.assertFalse(self.connector._closed)
        conn.close()
        self.assertTrue(self.connector._closed)

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_multiple_times(self, ClientRequestMock):
        req = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        conn = self.loop.run_until_complete(self.connector.connect(req, [], None))
        
        conn.close()
        with self.assertRaises(RuntimeError):
            conn.close()

    @mock.patch('aiohttp.connector.ClientRequest')
    def test_close_with_active_connections(self, ClientRequestMock):
        req1 = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        req2 = ClientRequest("GET", URL("http://www.python.org"), loop=self.loop)
        
        conn1 = self.loop.run_until_complete(self.connector.connect(req1, [], None))
        conn2 = self.loop.run_until_complete(self.connector.connect(req2, [], None))
        
        conn1.close()
        conn2.close()
        
        self.assertTrue(self.connector._closed)

    def tearDown(self):
        self.loop.run_until_complete(self.connector.close())