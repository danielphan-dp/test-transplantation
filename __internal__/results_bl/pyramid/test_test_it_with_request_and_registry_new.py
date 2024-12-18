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
        self.manager.set({'cookie': 'test_cookie'})
        result = self.manager.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_method_with_no_cookie(self):
        self.manager.set({})
        result = self.manager.get('cookie')
        self.assertIsNone(result)

    def test_get_method_with_invalid_name(self):
        self.manager.set({'cookie': 'test_cookie'})
        result = self.manager.get('invalid_name')
        self.assertIsNone(result)

    def test_get_method_after_closer_called(self):
        self.manager.set({'cookie': 'test_cookie'})
        closer = self.manager.get_closer()
        closer()
        result = self.manager.get('cookie')
        self.assertIsNone(result)

    def test_get_method_with_multiple_calls(self):
        self.manager.set({'cookie': 'test_cookie'})
        first_call = self.manager.get('cookie')
        second_call = self.manager.get('cookie')
        self.assertEqual(first_call, second_call)
        self.assertEqual(first_call, 'test_cookie')