import unittest
from http.cookies import SimpleCookie

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_empty_cookie(self):
        cookie = SimpleCookie()
        result = self.helper._cookieValue(cookie)
        self.assertEqual(result, {})

    def test_single_key_value(self):
        cookie = SimpleCookie()
        cookie['test'] = 'value'
        result = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(result, {'test': 'value'})

    def test_multiple_key_value(self):
        cookie = SimpleCookie()
        cookie['key1'] = 'value1'
        cookie['key2'] = 'value2'
        result = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_invalid_format(self):
        cookie = 'invalid_format'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie)

    def test_missing_value(self):
        cookie = SimpleCookie()
        cookie['key'] = ''
        result = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(result, {'key': ''})

    def test_extra_equals(self):
        cookie = SimpleCookie()
        cookie['key=value'] = 'value'
        result = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(result, {'key=value': 'value'})