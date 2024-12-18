import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import get_current_registry, manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.cookie_value = "test_cookie"
        self.dummy_request = DummyRequest(cookie=self.cookie_value)

    def test_get_cookie(self):
        result = self.dummy_request.cookies.get("session-token")
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existent_cookie(self):
        result = self.dummy_request.cookies.get("non-existent-cookie")
        self.assertIsNone(result)

    def test_get_cookie_with_hyphen(self):
        self.dummy_request.cookies = DummyCookies({"session-token": ["abc123"]})
        result = self.dummy_request.cookies.get("session-token")
        self.assertEqual(result, "abc123")

    def test_get_cookie_with_special_characters(self):
        self.dummy_request.cookies = DummyCookies({"session@token": ["special_value"]})
        result = self.dummy_request.cookies.get("session@token")
        self.assertEqual(result, "special_value")

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
        self.cookies = DummyCookies(cookie)