import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import prepare
from pyramid.threadlocal.manager import get_current_request

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({'Cookie': 'foo=one; foo=two'})
        self.registry = self._makeRegistry()
        self.manager = manager

    def test_get_cookie_value(self):
        cookie_value = self.manager.get('foo')
        self.assertEqual(cookie_value, 'one')

    def test_get_non_existent_cookie(self):
        cookie_value = self.manager.get('bar')
        self.assertIsNone(cookie_value)

    def test_get_multiple_cookie_values(self):
        cookie_values = self.manager.get('foo')
        self.assertIn('one', cookie_values)
        self.assertIn('two', cookie_values)

    def test_get_with_empty_request(self):
        empty_request = DummyRequest({})
        cookie_value = self.manager.get('foo', request=empty_request)
        self.assertIsNone(cookie_value)

    def test_get_with_invalid_registry(self):
        with self.assertRaises(ConfigurationError):
            self.manager.get('foo', registry=None)

    def _makeRegistry(self):
        # Mock registry creation logic
        return {}

    def _callFUT(self, request, registry):
        # Mock function call logic
        return {'root': self._makeRoot(), 'closer': lambda: None}

    def _makeRoot(self):
        # Mock root creation logic
        return DummyRoot()

class DummyRequest:
    def __init__(self, environ):
        self.environ = environ
        self.cookies = DummyCookies(environ.get('Cookie', ''))

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        if name in self.cookie:
            return self.cookie.split('=')[1].split(';')[0]
        return None

class DummyRoot:
    pass