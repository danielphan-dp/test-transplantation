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
        self.assertEqual(result[0]['max-age'], '500')

    def test_parse_headers_multiple(self):
        headers = [
            'Set-Cookie: userid=123; Max-Age=500',
            'Set-Cookie: sessionid=abc; Max-Age=300'
        ]
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['max-age'], '500')
        self.assertEqual(result[1]['max-age'], '300')

    def test_parse_headers_invalid_format(self):
        headers = ['InvalidHeaderFormat']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0].get('max-age'))

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)