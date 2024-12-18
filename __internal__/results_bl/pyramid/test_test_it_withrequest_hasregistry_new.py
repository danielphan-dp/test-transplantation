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
        self.request.cookies = {'session_id': 'abc123'}
        result = self.manager.get('session_id')
        self.assertEqual(result, 'abc123')

    def test_get_method_with_nonexistent_cookie(self):
        result = self.manager.get('nonexistent_cookie')
        self.assertIsNone(result)

    def test_get_method_with_empty_cookie(self):
        self.request.cookies = {}
        result = self.manager.get('session_id')
        self.assertIsNone(result)

    def test_get_method_with_multiple_cookies(self):
        self.request.cookies = {'session_id': 'abc123', 'user_id': 'user456'}
        result = self.manager.get('user_id')
        self.assertEqual(result, 'user456')

    def test_get_method_with_invalid_name(self):
        with self.assertRaises(ConfigurationError):
            self.manager.get(None)

    def test_get_method_registry_check(self):
        self.request.registry = self.registry
        result = self.manager.get()
        self.assertEqual(result['registry'], self.registry)

    def tearDown(self):
        self.manager = None
        self.request = None
        self.registry = None

if __name__ == '__main__':
    unittest.main()