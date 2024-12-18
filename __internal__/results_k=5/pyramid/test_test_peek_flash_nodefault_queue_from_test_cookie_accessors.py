import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie', 'fallback_value')
        self.assertEqual(result, 'fallback_value')

    def test_get_empty_cookie(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie', 'fallback_value')
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        self.request.cookies['special_cookie'] = 'value_with_special_chars_!@#$%^&*()'
        result = self.request.cookies.get('special_cookie')
        self.assertEqual(result, 'value_with_special_chars_!@#$%^&*()')

    def test_get_cookie_with_none_value(self):
        self.request.cookies['none_cookie'] = None
        result = self.request.cookies.get('none_cookie', 'fallback_value')
        self.assertEqual(result, 'fallback_value')

if __name__ == '__main__':
    unittest.main()