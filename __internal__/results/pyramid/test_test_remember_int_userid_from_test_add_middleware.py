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
        headers = ['Set-Cookie: userid=1; user_data=userid_type:int']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertIn('userid', result[0])
        self.assertEqual(result[0]['userid'], '1')

    def test_parse_headers_multiple(self):
        headers = [
            'Set-Cookie: userid=1; user_data=userid_type:int',
            'Set-Cookie: userid=2; user_data=userid_type:int'
        ]
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertIn('userid', result[0])
        self.assertEqual(result[0]['userid'], '1')
        self.assertIn('userid', result[1])
        self.assertEqual(result[1]['userid'], '2')

    def test_parse_headers_invalid_format(self):
        headers = ['InvalidHeaderFormat']
        with self.assertRaises(ValueError):
            self.helper._parseHeaders(headers)

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)

if __name__ == '__main__':
    unittest.main()