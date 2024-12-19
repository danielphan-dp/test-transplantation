import unittest
from pyramid.request import Request
from pyramid.response import Response

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = Request({})
        self.request.cookie = 'test_cookie_value'
    
    def test_get_method_returns_cookie(self):
        result = self.request.get('cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_nonexistent_name(self):
        result = self.request.get('nonexistent_name')
        self.assertIsNone(result)

    def test_get_method_with_empty_name(self):
        result = self.request.get('')
        self.assertIsNone(result)

    def test_get_method_with_special_characters(self):
        self.request.cookie = 'cookie_with_special_chars_!@#$%^&*()'
        result = self.request.get('cookie')
        self.assertEqual(result, 'cookie_with_special_chars_!@#$%^&*()')