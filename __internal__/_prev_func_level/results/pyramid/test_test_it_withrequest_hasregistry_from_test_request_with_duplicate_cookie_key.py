import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import prepare
from pyramid.config import global_registries

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.registry = self.request.registry = self._makeRegistry()
        self.manager = manager

    def test_get_method_returns_cookie(self):
        cookie_value = 'test_cookie_value'
        self.request.cookies = DummyCookies(cookie_value)
        result = self.manager.get('test_cookie')
        self.assertEqual(result, cookie_value)

    def test_get_method_with_no_cookie(self):
        self.request.cookies = DummyCookies(None)
        result = self.manager.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_method_with_duplicate_cookie_keys(self):
        cookie_value = 'foo=one; foo=two'
        self.request.cookies = DummyCookies(cookie_value)
        result = self.manager.get('foo')
        self.assertEqual(result, 'one')

    def test_get_method_with_empty_cookie(self):
        self.request.cookies = DummyCookies('')
        result = self.manager.get('empty_cookie')
        self.assertIsNone(result)

    def test_get_method_with_invalid_cookie_format(self):
        cookie_value = 'invalid_cookie_format'
        self.request.cookies = DummyCookies(cookie_value)
        result = self.manager.get('invalid_cookie')
        self.assertIsNone(result)

    def _makeRegistry(self):
        return global_registries

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        if self.cookie:
            cookies = self.cookie.split('; ')
            for c in cookies:
                key, value = c.split('=')
                if key == name:
                    return value
        return None

class DummyRequest:
    def __init__(self, environ=None, session=None, registry=None, cookie=None):
        self.environ = environ or {}
        self.session = session or {}
        self.registry = registry
        self.cookies = DummyCookies(cookie)