import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.helper = DummyCookies('test_cookie_value')

    def test_get_existing_cookie(self):
        result = self.helper.get('test_cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.helper.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        empty_helper = DummyCookies('')
        result = empty_helper.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_with_none_name(self):
        result = self.helper.get(None)
        self.assertIsNone(result)

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie if name == 'test_cookie' else None