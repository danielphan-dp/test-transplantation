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

    def test_get_with_default_value(self):
        result = self.request.cookies.get('another_cookie', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_get_empty_cookie(self):
        self.request.cookies['empty_cookie'] = ''
        result = self.request.cookies.get('empty_cookie', 'fallback')
        self.assertEqual(result, '')

    def test_get_none_cookie(self):
        result = self.request.cookies.get(None, 'fallback')
        self.assertEqual(result, 'fallback')