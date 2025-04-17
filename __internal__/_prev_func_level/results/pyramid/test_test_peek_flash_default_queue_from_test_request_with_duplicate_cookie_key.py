import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'cookie_value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_with_multiple_cookies(self):
        self.request.cookies = {'cookie1': 'value1', 'cookie2': 'value2'}
        result1 = self.request.cookies.get('cookie1')
        result2 = self.request.cookies.get('cookie2')
        self.assertEqual(result1, 'value1')
        self.assertEqual(result2, 'value2')

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get('empty_cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'special_cookie': 'value_with_special_chars_!@#$%^&*()'}
        result = self.request.cookies.get('special_cookie')
        self.assertEqual(result, 'value_with_special_chars_!@#$%^&*()')