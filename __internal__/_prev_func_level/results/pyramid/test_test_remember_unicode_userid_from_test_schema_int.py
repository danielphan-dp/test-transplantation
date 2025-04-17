import unittest
from pyramid.testing import DummyRequest

class TestParseHeaders(unittest.TestCase):
    def setUp(self):
        self.helper = self._makeOne('secret')

    def _makeOne(self, secret):
        class Helper:
            def _parseHeader(self, header):
                return {'header': header}
        return Helper()

    def test_parse_headers_empty(self):
        headers = []
        result = self.helper._parseHeaders(headers)
        self.assertEqual(result, [])

    def test_parse_headers_single(self):
        headers = ['Authorization: Bearer token']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {'header': 'Authorization: Bearer token'})

    def test_parse_headers_multiple(self):
        headers = ['Header1: value1', 'Header2: value2']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'header': 'Header1: value1'})
        self.assertEqual(result[1], {'header': 'Header2: value2'})

    def test_parse_headers_invalid(self):
        headers = [None, '', 'InvalidHeader']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {'header': None})
        self.assertEqual(result[1], {'header': ''})
        self.assertEqual(result[2], {'header': 'InvalidHeader'})