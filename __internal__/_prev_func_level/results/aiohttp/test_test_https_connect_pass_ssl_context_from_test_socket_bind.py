import asyncio
import unittest
from unittest import mock
from aiohttp import ClientRequest, ClientResponse, TCPConnector, ClientTimeout
from yarl import URL

class TestConnectorClose(unittest.TestCase):
    @mock.patch('aiohttp.connector.ClientRequest')
    @mock.patch('aiohttp.connector.aiohappyeyeballs.start_connection', autospec=True, spec_set=True)
    def test_connector_close(self, start_connection: mock.Mock, ClientRequestMock: mock.Mock) -> None:
        connector = TCPConnector()
        self.assertFalse(connector._closed)

        # Close the connector
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)

        # Attempt to close again and ensure no errors are raised
        asyncio.run(connector.close())
        self.assertTrue(connector._closed)

        # Create a request to ensure it raises an error when closed
        req = ClientRequest("GET", URL("http://example.com"), connector=connector)
        with self.assertRaises(RuntimeError):
            asyncio.run(req.close())

        # Ensure that the connector is still closed
        self.assertTrue(connector._closed)

if __name__ == '__main__':
    unittest.main()