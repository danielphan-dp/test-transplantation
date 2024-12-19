import unittest
from http.cookies import SimpleCookie
from pyramid.util import text_

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_empty_cookie(self):
        cookie = SimpleCookie()
        cookie_value = self.helper._cookieValue(cookie)
        self.assertEqual(cookie_value, {})

    def test_single_key_value(self):
        cookie = SimpleCookie()
        cookie['test'] = 'value'
        cookie_value = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(cookie_value, {'test': 'value'})

    def test_multiple_key_value(self):
        cookie = SimpleCookie()
        cookie['key1'] = 'value1'
        cookie['key2'] = 'value2'
        cookie_value = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(cookie_value, {'key1': 'value1', 'key2': 'value2'})

    def test_invalid_format(self):
        cookie = SimpleCookie()
        cookie['invalid'] = 'value1=value2=value3'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie.output(header='', sep='').strip())

    def test_unicode_key_value(self):
        cookie = SimpleCookie()
        cookie['userid'] = text_(b'\xc2\xa9', 'utf-8')
        cookie_value = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(cookie_value['userid'], text_(b'\xc2\xa9', 'utf-8'))

    def test_special_characters(self):
        cookie = SimpleCookie()
        cookie['key!@#'] = 'value$%^'
        cookie_value = self.helper._cookieValue(cookie.output(header='', sep='').strip())
        self.assertEqual(cookie_value, {'key!@#': 'value$%^'})