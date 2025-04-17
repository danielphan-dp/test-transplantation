import unittest
from http.cookies import SimpleCookie
from pyramid.util import text_

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_cookie_value_valid(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key=value'
        val = self.helper._cookieValue(cookie['test'])
        self.assertEqual(val['key'], 'value')

    def test_cookie_value_multiple_items(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key1=value1/key2=value2'
        val = self.helper._cookieValue(cookie['test'])
        self.assertEqual(val['key1'], 'value1')
        self.assertEqual(val['key2'], 'value2')

    def test_cookie_value_no_value(self):
        cookie = SimpleCookie()
        cookie['test'] = 'key='
        val = self.helper._cookieValue(cookie['test'])
        self.assertEqual(val['key'], '')

    def test_cookie_value_invalid_format(self):
        cookie = SimpleCookie()
        cookie['test'] = 'invalid_format'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie['test'])

    def test_cookie_value_empty_cookie(self):
        cookie = SimpleCookie()
        cookie['test'] = ''
        val = self.helper._cookieValue(cookie['test'])
        self.assertEqual(val, {})

    def _makeOne(self, secret):
        # Mocking the helper creation
        return MockHelper(secret)

class MockHelper:
    def __init__(self, secret):
        self.secret = secret

    def _cookieValue(self, cookie):
        items = cookie.value.split('/')
        D = {}
        for item in items:
            if '=' in item:
                k, v = item.split('=', 1)
                D[k] = v
            else:
                raise ValueError("Invalid cookie format")
        return D