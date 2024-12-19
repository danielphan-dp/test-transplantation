import unittest
from http.cookies import SimpleCookie
from pyramid.authentication import AuthTktCookieHelper

class TestAuthTktCookieHelper(unittest.TestCase):

    def setUp(self):
        self.helper = AuthTktCookieHelper()

    def test_get_cookie(self):
        cookie_name = 'test_cookie'
        self.helper.cookie = SimpleCookie()
        self.helper.cookie[cookie_name] = 'test_value'
        result = self.helper.get(cookie_name)
        self.assertEqual(result, self.helper.cookie)

    def test_get_non_existent_cookie(self):
        cookie_name = 'non_existent_cookie'
        self.helper.cookie = SimpleCookie()
        result = self.helper.get(cookie_name)
        self.assertEqual(result, self.helper.cookie)

    def test_get_empty_cookie(self):
        cookie_name = 'empty_cookie'
        self.helper.cookie = SimpleCookie()
        self.helper.cookie[cookie_name] = ''
        result = self.helper.get(cookie_name)
        self.assertEqual(result, self.helper.cookie)

    def test_get_cookie_with_special_characters(self):
        cookie_name = 'special_cookie'
        self.helper.cookie = SimpleCookie()
        self.helper.cookie[cookie_name] = 'value_with_special_chars_!@#$%^&*()'
        result = self.helper.get(cookie_name)
        self.assertEqual(result, self.helper.cookie)