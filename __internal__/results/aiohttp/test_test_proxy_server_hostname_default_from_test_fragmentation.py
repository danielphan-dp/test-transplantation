import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestClientRequestClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_client_request_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        request = ClientRequest("GET", URL("http://example.com"))
        ClientRequestMock.return_value = request

        response = ClientResponse(
            "get",
            URL("http://example.com"),
            request_info=mock.Mock(),
            writer=None,
            continue100=None,
            timer=mock.Mock(),
            traces=[],
            loop=asyncio.get_event_loop(),
            session=mock.Mock(),
        )

        with mock.patch.object(request, "send", autospec=True, return_value=response):
            with mock.patch.object(response, "start", autospec=True) as m:
                m.return_value.status = 200

                async def make_connector() -> TCPConnector:
                    return TCPConnector()

                connector = asyncio.get_event_loop().run_until_complete(make_connector())
                asyncio.get_event_loop().run_until_complete(connector._create_connection(request, [], ClientTimeout()))

                asyncio.get_event_loop().run_until_complete(request.close())
                self.assertTrue(request.closed)

                asyncio.get_event_loop().run_until_complete(connector.close())