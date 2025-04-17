import unittest
from pyramid.authentication import AuthTktCookieHelper

class TestAuthTktCookieHelper(unittest.TestCase):

    def setUp(self):
        self.helper = AuthTktCookieHelper('secret')

    def test_parse_headers_empty(self):
        result = self.helper._parseHeaders([])
        self.assertEqual(result, [])

    def test_parse_headers_single(self):
        headers = ['Set-Cookie: userid=123; Max-Age=500']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertIn('Max-Age', result[0])
        self.assertEqual(result[0]['Max-Age'], '500')

    def test_parse_headers_multiple(self):
        headers = [
            'Set-Cookie: userid=123; Max-Age=500',
            'Set-Cookie: sessionid=abc; Max-Age=300'
        ]
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertIn('Max-Age', result[0])
        self.assertIn('Max-Age', result[1])
        self.assertEqual(result[0]['Max-Age'], '500')
        self.assertEqual(result[1]['Max-Age'], '300')

    def test_parse_headers_invalid(self):
        headers = ['InvalidHeader']
        with self.assertRaises(Exception):
            self.helper._parseHeaders(headers)

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)