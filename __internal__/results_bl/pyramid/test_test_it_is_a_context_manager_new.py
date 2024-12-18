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
        self.manager = get_root(self.request)

    def test_get_returns_cookie(self):
        expected_cookie = 'test_cookie'
        self.manager.cookie = expected_cookie
        result = self.manager.get('test_name')
        self.assertEqual(result, expected_cookie)

    def test_get_with_nonexistent_name(self):
        result = self.manager.get('nonexistent_name')
        self.assertIsNone(result)

    def test_get_with_empty_name(self):
        result = self.manager.get('')
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        special_name = '@#$%^&*()'
        self.manager.cookie = 'special_cookie'
        result = self.manager.get(special_name)
        self.assertEqual(result, 'special_cookie')

    def test_get_does_not_modify_registry(self):
        original_registry = self.registry
        self.manager.get('test_name')
        self.assertEqual(self.registry, original_registry)

    def test_get_with_none_request(self):
        self.manager.request = None
        with self.assertRaises(ConfigurationError):
            self.manager.get('test_name')