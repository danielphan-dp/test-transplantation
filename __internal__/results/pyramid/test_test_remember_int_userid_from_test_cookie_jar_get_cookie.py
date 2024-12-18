import unittest
from http.cookies import SimpleCookie

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_cookie_value_with_valid_cookie(self):
        cookie = SimpleCookie()
        cookie['userid'] = '1'
        cookie['user_data'] = 'userid_type:int'
        result = self.helper._cookieValue(cookie.output(header='', sep=''))
        self.assertEqual(result['userid'], '1')
        self.assertEqual(result['user_data'], 'userid_type:int')

    def test_cookie_value_with_missing_key(self):
        cookie = SimpleCookie()
        cookie['userid'] = '1'
        result = self.helper._cookieValue(cookie.output(header='', sep=''))
        self.assertNotIn('user_data', result)

    def test_cookie_value_with_empty_cookie(self):
        cookie = SimpleCookie()
        result = self.helper._cookieValue(cookie.output(header='', sep=''))
        self.assertEqual(result, {})

    def test_cookie_value_with_invalid_format(self):
        cookie = SimpleCookie()
        cookie['invalid'] = 'no_equals_sign'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie.output(header='', sep=''))

    def test_cookie_value_with_multiple_items(self):
        cookie = SimpleCookie()
        cookie['userid'] = '1'
        cookie['user_data'] = 'userid_type:int'
        cookie['session'] = 'abc123'
        result = self.helper._cookieValue(cookie.output(header='', sep=''))
        self.assertEqual(result['userid'], '1')
        self.assertEqual(result['user_data'], 'userid_type:int')
        self.assertEqual(result['session'], 'abc123')