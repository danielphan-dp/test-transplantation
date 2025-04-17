import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def _makeRequest(self, cookie_value):
        class DummyCookies:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        class DummyRequest:
            def __init__(self, cookie):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie_value)

    def _makeOne(self):
        class DummyHelper:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        return DummyHelper

    def test_get_existing_cookie(self):
        request = self._makeRequest('test_cookie_value')
        helper = self._makeOne()('test_cookie_value')
        result = helper.get('cookie_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        request = self._makeRequest(None)
        helper = self._makeOne()(None)
        result = helper.get('cookie_name')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        request = self._makeRequest('')
        helper = self._makeOne()('')
        result = helper.get('cookie_name')
        self.assertEqual(result, '')

    def test_get_cookie_with_special_characters(self):
        request = self._makeRequest('cookie_with_special_chars_!@#$%^&*()')
        helper = self._makeOne()('cookie_with_special_chars_!@#$%^&*()')
        result = helper.get('cookie_name')
        self.assertEqual(result, 'cookie_with_special_chars_!@#$%^&*()')