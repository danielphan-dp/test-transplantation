import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import prepare
from pyramid.threadlocal.manager import get_current_request

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({'cookie': 'test_cookie'})
        self.registry = self.request.registry = self._makeRegistry()
        self.manager = manager

    def _makeRegistry(self):
        return {}

    def test_get_cookie(self):
        cookie_value = self.request.cookies.get('cookie')
        self.assertEqual(cookie_value, 'test_cookie')

    def test_get_non_existent_cookie(self):
        cookie_value = self.request.cookies.get('non_existent_cookie')
        self.assertIsNone(cookie_value)

    def test_get_with_empty_request(self):
        empty_request = DummyRequest({})
        cookie_value = empty_request.cookies.get('cookie')
        self.assertIsNone(cookie_value)

    def test_get_with_different_cookie(self):
        self.request.cookies = DummyCookies({"session-token": ["abc123"]})
        cookie_value = self.request.cookies.get("session-token")
        self.assertEqual(cookie_value, "abc123")

    def test_get_with_invalid_cookie_name(self):
        cookie_value = self.request.cookies.get("")
        self.assertIsNone(cookie_value)

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