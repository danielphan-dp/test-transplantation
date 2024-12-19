import unittest
import warnings
from pyramid.authentication import AuthTktCookieHelper

class TestAuthTktCookieHelper(unittest.TestCase):

    def setUp(self):
        self.helper = AuthTktCookieHelper('secret')

    def test_parse_headers_empty(self):
        result = self.helper._parseHeaders([])
        self.assertEqual(result, [])

    def test_parse_headers_single_valid(self):
        headers = ['userid=valid_user']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 1)
        self.assertTrue('userid' in result[0].value)

    def test_parse_headers_multiple_valid(self):
        headers = ['userid=user1', 'userid=user2']
        result = self.helper._parseHeaders(headers)
        self.assertEqual(len(result), 2)
        self.assertTrue('userid' in result[0].value)
        self.assertTrue('userid' in result[1].value)

    def test_parse_headers_invalid_format(self):
        headers = ['invalid_header']
        with self.assertRaises(ValueError):
            self.helper._parseHeaders(headers)

    def test_parse_headers_none(self):
        with self.assertRaises(TypeError):
            self.helper._parseHeaders(None)

    def test_parse_headers_warning_on_invalid_userid(self):
        headers = ['userid=']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always', RuntimeWarning)
            result = self.helper._parseHeaders(headers)
            self.assertTrue(str(w[-1].message).startswith('userid is of type'))
        self.assertEqual(len(result), 1)
        self.assertTrue('userid' in result[0].value)

if __name__ == '__main__':
    unittest.main()