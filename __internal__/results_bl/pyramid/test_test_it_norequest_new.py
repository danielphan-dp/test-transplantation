import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = self._makeRegistry()
        self.app = DummyApp(registry=self.registry)
        self.root, self.closer = self._callFUT(self.app)

    def tearDown(self):
        self.closer()

    def test_get_method_returns_cookie(self):
        expected_cookie = 'test_cookie'
        self.app.cookie = expected_cookie
        result = self.app.get('test_name')
        self.assertEqual(result, expected_cookie)

    def test_get_method_with_no_cookie(self):
        self.app.cookie = None
        result = self.app.get('test_name')
        self.assertIsNone(result)

    def test_get_method_with_different_name(self):
        self.app.cookie = 'another_cookie'
        result = self.app.get('different_name')
        self.assertEqual(result, 'another_cookie')

    def test_get_method_registry_access(self):
        pushed = manager.get()
        self.assertEqual(pushed['registry'], self.registry)

    def test_get_method_request_environ(self):
        pushed = manager.get()
        self.assertEqual(pushed['request'].environ['path'], '/')