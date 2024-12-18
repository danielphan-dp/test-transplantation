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

    def test_get_empty_cookie(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_multiple_cookies(self):
        self.request.cookies['foo'] = 'one'
        self.request.cookies['foo'] = 'two'
        result = self.request.cookies.get('foo')
        self.assertEqual(result, 'two')  # Last value should be returned

    def test_get_cookie_with_special_characters(self):
        self.request.cookies['special_cookie'] = 'value_with_special_chars_!@#$%^&*()'
        result = self.request.cookies.get('special_cookie')
        self.assertEqual(result, 'value_with_special_chars_!@#$%^&*()')