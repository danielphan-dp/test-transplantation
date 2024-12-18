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
        self.assertIn('userid', result[0])
        self.assertEqual(result[0]['userid'], '123')
        self.assertEqual(result[0]['max-age'], '500')

    def test_parse_headers_multiple(self):
        headers = [
            'Set-Cookie: userid=123; Max-Age=500',
            'Set-Cookie: sessionid=abc; Max-Age=300'
        ]
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertIn('userid', result[0])
        self.assertIn('sessionid', result[1])
        self.assertEqual(result[0]['userid'], '123')
        self.assertEqual(result[1]['sessionid'], 'abc')

    def test_parse_headers_invalid(self):
        headers = ['InvalidHeader']
        with self.assertRaises(Exception):
            self.helper._parseHeaders(headers)

    def test_parse_headers_with_expires(self):
        headers = ['Set-Cookie: userid=123; Max-Age=500; Expires=Wed, 21 Oct 2025 07:28:00 GMT']
        result = self.helper._parseHeaders(headers)
        self.assertTrue('expires' in result[0])
        self.assertEqual(result[0]['expires'], 'Wed, 21 Oct 2025 07:28:00 GMT')