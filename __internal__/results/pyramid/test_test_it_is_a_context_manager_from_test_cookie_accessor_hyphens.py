import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.manager = DummyCookieHelper("test_cookie_value")

    def test_get_method_returns_cookie(self):
        result = self.manager.get("test_cookie")
        self.assertEqual(result, "test_cookie_value")

    def test_get_method_with_non_existent_cookie(self):
        result = self.manager.get("non_existent_cookie")
        self.assertIsNone(result)

    def test_get_method_with_empty_name(self):
        result = self.manager.get("")
        self.assertIsNone(result)

    def test_get_method_with_special_characters(self):
        self.manager = DummyCookieHelper({"session-token": ["abc123"]})
        result = self.manager.get("session-token")
        self.assertEqual(result, "abc123")

    def test_get_method_with_hyphenated_cookie(self):
        self.manager = DummyCookieHelper({"session-token": ["xyz789"]})
        result = self.manager.get("session-token")
        self.assertEqual(result, "xyz789")

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie.get(name)

class DummyRequest:
    def __init__(self, environ=None, session=None, registry=None, cookie=None):
        self.environ = environ or {}
        self.session = session or {}
        self.registry = registry
        self.cookies = DummyCookies(cookie) if cookie else DummyCookies({})