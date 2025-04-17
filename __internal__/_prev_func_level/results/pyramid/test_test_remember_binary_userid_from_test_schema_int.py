import unittest
from pyramid.authentication import AuthTktCookieHelper

class TestAuthTktCookieHelper(unittest.TestCase):

    def setUp(self):
        self.helper = AuthTktCookieHelper('secret')

    def test_parse_headers_empty(self):
        headers = []
        result = self.helper._parseHeaders(headers)
        self.assertEqual(result, [])

    def test_parse_headers_single(self):
        headers = ['Set-Cookie: test=value']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'Set-Cookie: test=value')

    def test_parse_headers_multiple(self):
        headers = ['Set-Cookie: test1=value1', 'Set-Cookie: test2=value2']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'Set-Cookie: test1=value1')
        self.assertEqual(result[1], 'Set-Cookie: test2=value2')

    def test_parse_headers_invalid(self):
        headers = ['InvalidHeader']
        with self.assertRaises(Exception):
            self.helper._parseHeaders(headers)

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)