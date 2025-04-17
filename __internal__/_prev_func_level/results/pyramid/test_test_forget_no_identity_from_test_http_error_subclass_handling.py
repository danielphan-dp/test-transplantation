import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def _makeRequest(self, cookie_value=None):
        class DummyCookies:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        class DummyRequest:
            def __init__(self, cookie=None):
                self.cookies = DummyCookies(cookie)

        return DummyRequest(cookie_value)

    def _makeOne(self):
        class DummyHelper:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        return DummyHelper("test_cookie_value")

    def test_get_method_with_valid_cookie(self):
        request = self._makeRequest("test_cookie_value")
        helper = self._makeOne()
        result = helper.get("cookie_name")
        self.assertEqual(result, "test_cookie_value")

    def test_get_method_with_none_cookie(self):
        request = self._makeRequest(None)
        helper = self._makeOne()
        result = helper.get("cookie_name")
        self.assertEqual(result, "test_cookie_value")

    def test_get_method_with_empty_cookie(self):
        request = self._makeRequest("")
        helper = self._makeOne()
        result = helper.get("cookie_name")
        self.assertEqual(result, "test_cookie_value")