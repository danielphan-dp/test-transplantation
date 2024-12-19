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

class TestProxyServer(unittest.TestCase):

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        proxy_req = ClientRequest("GET", URL("http://proxy.example.com"), loop=asyncio.get_event_loop())
        ClientRequestMock.return_value = proxy_req

        proxy_resp = ClientResponse(
            "get",
            URL("http://proxy.example.com"),
            request_info=mock.Mock(),
            writer=None,
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=asyncio.get_event_loop(),
            session=mock.Mock(),
        )

        with mock.patch.object(proxy_req, "send", autospec=True, return_value=proxy_resp):
            with mock.patch.object(proxy_resp, "start", autospec=True) as m:
                m.return_value.status = 200

                async def make_conn() -> aiohttp.TCPConnector:
                    return aiohttp.TCPConnector()

                connector = asyncio.get_event_loop().run_until_complete(make_conn())
                r = {
                    "hostname": "hostname",
                    "host": "127.0.0.1",
                    "port": 80,
                    "family": socket.AF_INET,
                    "proto": 0,
                    "flags": 0,
                }
                with mock.patch.object(connector, "_resolve_host", autospec=True, return_value=[r]):
                    tr, proto = mock.Mock(), mock.Mock()
                    with mock.patch.object(asyncio.get_event_loop(), "create_connection", autospec=True, return_value=(tr, proto)):
                        with mock.patch.object(asyncio.get_event_loop(), "start_tls", autospec=True, return_value=mock.Mock()) as tls_m:
                            req = ClientRequest(
                                "GET",
                                URL("https://www.python.org"),
                                proxy=URL("http://proxy.example.com"),
                                loop=asyncio.get_event_loop(),
                            )
                            asyncio.get_event_loop().run_until_complete(connector._create_connection(req, [], aiohttp.ClientTimeout()))

                            asyncio.get_event_loop().run_until_complete(proxy_req.close())
                            proxy_resp.close()
                            asyncio.get_event_loop().run_until_complete(req.close())
                            asyncio.get_event_loop().run_until_complete(connector.close())

                            # Test close method directly
                            connector.close()
                            self.assertIsNone(connector._connector)  # Assuming _connector is set to None on close

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method_multiple_calls(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = asyncio.get_event_loop().run_until_complete(aiohttp.TCPConnector())
        asyncio.get_event_loop().run_until_complete(connector.close())
        with self.assertRaises(RuntimeError):
            asyncio.get_event_loop().run_until_complete(connector.close())  # Ensure it raises on second close

    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_close_method_with_active_connections(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = asyncio.get_event_loop().run_until_complete(aiohttp.TCPConnector())
        # Simulate an active connection
        connector._active_connections = 1  # Assuming this is how active connections are tracked
        with self.assertRaises(RuntimeError):
            asyncio.get_event_loop().run_until_complete(connector.close())  # Ensure it raises if there are active connections