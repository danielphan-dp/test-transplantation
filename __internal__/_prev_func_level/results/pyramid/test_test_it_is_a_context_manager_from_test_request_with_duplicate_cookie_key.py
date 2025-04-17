import unittest
from pyramid.scripting import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.manager = DummyCookies("test_cookie_value")

    def test_get_returns_cookie_value(self):
        result = self.manager.get("test_cookie")
        self.assertEqual(result, "test_cookie_value")

    def test_get_with_nonexistent_cookie(self):
        result = self.manager.get("nonexistent_cookie")
        self.assertIsNone(result)

    def test_get_with_empty_cookie(self):
        empty_manager = DummyCookies("")
        result = empty_manager.get("test_cookie")
        self.assertEqual(result, "")

    def test_get_with_multiple_cookies(self):
        multiple_cookies = DummyCookies("foo=one; foo=two; bar=three")
        result_foo = multiple_cookies.get("foo")
        result_bar = multiple_cookies.get("bar")
        self.assertEqual(result_foo, "one")
        self.assertEqual(result_bar, "three")

    def test_get_with_invalid_cookie_format(self):
        invalid_cookie = DummyCookies("invalid_cookie_format")
        result = invalid_cookie.get("test_cookie")
        self.assertEqual(result, "invalid_cookie_format")