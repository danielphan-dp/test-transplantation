import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_cookie_value(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get('non_existent_cookie')
        self.assertIsNone(result)

    def test_get_with_registry(self):
        self._callFUT(registry=self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

    def _callFUT(self, registry):
        self.request.registry = registry
        return self.request.get('test_cookie')