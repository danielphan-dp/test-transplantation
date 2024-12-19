import unittest
from pyramid.authentication import AuthTktCookieHelper

class TestAuthTktCookieHelper(unittest.TestCase):

    def setUp(self):
        self.helper = AuthTktCookieHelper()

    def test_get_cookie(self):
        name = 'test_cookie'
        self.helper.cookie = 'cookie_value'
        result = self.helper.get(name)
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existent_cookie(self):
        name = 'non_existent_cookie'
        self.helper.cookie = None
        result = self.helper.get(name)
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        name = 'empty_cookie'
        self.helper.cookie = ''
        result = self.helper.get(name)
        self.assertEqual(result, '')