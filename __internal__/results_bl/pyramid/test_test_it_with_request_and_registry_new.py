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

    def test_get_method_returns_cookie(self):
        self.manager.set(self.request)
        cookie_value = self.manager.get('cookie')
        self.assertIsNotNone(cookie_value)

    def test_get_method_with_invalid_name(self):
        self.manager.set(self.request)
        with self.assertRaises(KeyError):
            self.manager.get('invalid_name')

    def test_get_method_after_closer_called(self):
        self.manager.set(self.request)
        self.manager.get('cookie')
        self.manager.close()
        with self.assertRaises(ConfigurationError):
            self.manager.get('cookie')

    def test_get_method_with_multiple_requests(self):
        request2 = DummyRequest({})
        self.manager.set(self.request)
        self.manager.set(request2)
        cookie_value1 = self.manager.get('cookie')
        cookie_value2 = self.manager.get('cookie')
        self.assertNotEqual(cookie_value1, cookie_value2)

    def tearDown(self):
        self.manager.close()