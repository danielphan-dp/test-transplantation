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

    def test_get_with_no_cookie_set(self):
        self.manager.cookie = None
        result = self.manager.get('test_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.manager.cookie = 'another_cookie'
        result = self.manager.get('different_name')
        self.assertEqual(result, 'another_cookie')

    def test_get_with_empty_name(self):
        self.manager.cookie = 'empty_name_cookie'
        result = self.manager.get('')
        self.assertEqual(result, 'empty_name_cookie')

    def test_get_with_nonexistent_name(self):
        self.manager.cookie = 'nonexistent_cookie'
        result = self.manager.get('nonexistent_name')
        self.assertEqual(result, 'nonexistent_cookie')