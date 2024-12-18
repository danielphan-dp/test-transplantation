import unittest
from http.cookies import SimpleCookie
from pyramid.util import text_

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_cookie_value_with_valid_cookie(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key=value'
        result = self.helper._cookieValue(cookie['test'])
        self.assertEqual(result, {'key': 'value'})

    def test_cookie_value_with_multiple_items(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key1=value1/key2=value2'
        result = self.helper._cookieValue(cookie['test'])
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_cookie_value_with_empty_string(self):
        cookie = SimpleCookie()
        cookie['test'] = ''
        result = self.helper._cookieValue(cookie['test'])
        self.assertEqual(result, {})

    def test_cookie_value_with_invalid_format(self):
        cookie = SimpleCookie()
        cookie['test'] = 'keyonly'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie['test'])

    def test_cookie_value_with_special_characters(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key1=value1/key2=val&ue2'
        result = self.helper._cookieValue(cookie['test'])
        self.assertEqual(result, {'key1': 'value1', 'key2': 'val&ue2'})