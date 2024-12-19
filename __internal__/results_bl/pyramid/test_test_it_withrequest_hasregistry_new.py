import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import _make_request
from pyramid.config import global_registries

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.registry = self._makeRegistry()
        self.manager = manager

    def test_get_returns_cookie(self):
        self.manager.set(self.request)
        cookie_value = self.manager.get('cookie')
        self.assertIsNotNone(cookie_value)

    def test_get_with_nonexistent_name(self):
        self.manager.set(self.request)
        with self.assertRaises(KeyError):
            self.manager.get('nonexistent_name')

    def test_get_with_empty_name(self):
        self.manager.set(self.request)
        cookie_value = self.manager.get('')
        self.assertIsNone(cookie_value)

    def test_get_after_closer_called(self):
        self.manager.set(self.request)
        closer = self.manager.get_closer()
        closer()
        with self.assertRaises(ConfigurationError):
            self.manager.get('cookie')

    def test_get_with_different_request(self):
        another_request = DummyRequest({})
        self.manager.set(another_request)
        cookie_value = self.manager.get('cookie')
        self.assertNotEqual(cookie_value, self.manager.get('cookie'))