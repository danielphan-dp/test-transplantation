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

    def test_get_method_with_valid_cookie(self):
        request = self._makeRequest('valid_cookie_value')
        helper = self._makeOne('valid_cookie_value')()
        result = helper.get('cookie_name')
        self.assertEqual(result, 'valid_cookie_value')

    def test_get_method_with_none_cookie(self):
        request = self._makeRequest(None)
        helper = self._makeOne(None)()
        result = helper.get('cookie_name')
        self.assertIsNone(result)

    def test_get_method_with_empty_string_cookie(self):
        request = self._makeRequest('')
        helper = self._makeOne('')()
        result = helper.get('cookie_name')
        self.assertEqual(result, '')

    def test_get_method_with_unexpected_cookie_name(self):
        request = self._makeRequest('some_cookie_value')
        helper = self._makeOne('some_cookie_value')()
        result = helper.get('non_existent_cookie_name')
        self.assertEqual(result, 'some_cookie_value')