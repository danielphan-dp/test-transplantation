import unittest
from pyramid.testing import DummyRequest

class TestParseHeaders(unittest.TestCase):
    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_parse_headers_empty(self):
        headers = []
        result = self.helper._parseHeaders(headers)
        self.assertEqual(result, [])

    def test_parse_headers_single_header(self):
        headers = ['Header1: Value1']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.helper._parseHeader('Header1: Value1'))

    def test_parse_headers_multiple_headers(self):
        headers = ['Header1: Value1', 'Header2: Value2']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.helper._parseHeader('Header1: Value1'))
        self.assertEqual(result[1], self.helper._parseHeader('Header2: Value2'))

    def test_parse_headers_invalid_header(self):
        headers = ['InvalidHeader']
        with self.assertRaises(SomeExpectedException):
            self.helper._parseHeaders(headers)

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)

    def _makeOne(self, secret):
        from pyramid.authentication import AuthTktCookieHelper
        return AuthTktCookieHelper(secret)