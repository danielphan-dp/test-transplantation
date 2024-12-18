import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}
        self.method_under_test = self.get_method

    def get_method(self, name):
        return self.request.cookies.get(name)

    def test_get_existing_cookie(self):
        result = self.method_under_test('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existing_cookie(self):
        result = self.method_under_test('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_with_registry(self):
        self._callFUT(registry=self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

    def _callFUT(self, registry):
        self.request.registry = registry
        return self.request

if __name__ == '__main__':
    unittest.main()