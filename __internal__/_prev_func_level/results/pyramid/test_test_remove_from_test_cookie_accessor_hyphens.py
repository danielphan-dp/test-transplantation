import unittest
from pyramid.registry import Registry

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.cookie_name = "session-token"
        self.cookie_value = "abc123"
        self.request = DummyRequest(cookie={self.cookie_name: self.cookie_value})

    def test_get_existing_cookie(self):
        cookies = DummyCookies(self.request.cookies)
        self.assertEqual(cookies.get(self.cookie_name), self.cookie_value)

    def test_get_non_existing_cookie(self):
        cookies = DummyCookies(self.request.cookies)
        self.assertIsNone(cookies.get("non-existing-cookie"))

    def test_get_cookie_with_hyphen(self):
        cookies = DummyCookies(self.request.cookies)
        self.assertEqual(cookies.get("session-token"), self.cookie_value)

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie.get(name)