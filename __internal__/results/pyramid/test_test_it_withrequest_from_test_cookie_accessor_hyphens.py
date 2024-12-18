import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import prepare
from pyramid.config import global_registries

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie.get(name)

class DummyRequest:
    def __init__(self, environ=None, cookies=None):
        self.environ = environ or {}
        self.cookies = cookies or DummyCookies({})

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest(cookies=DummyCookies({"session-token": "abc123"}))
        self.manager = manager

    def test_get_cookie(self):
        result = self.request.cookies.get("session-token")
        self.assertEqual(result, "abc123")

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get("non-existent-token")
        self.assertIsNone(result)

    def test_get_with_empty_cookie(self):
        empty_request = DummyRequest(cookies=DummyCookies({}))
        result = empty_request.cookies.get("session-token")
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = DummyCookies({"session-token": "abc@123"})
        result = self.request.cookies.get("session-token")
        self.assertEqual(result, "abc@123")