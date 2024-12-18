import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.cookie_value = "test_cookie"
        self.registry.cookie = self.cookie_value

    def _callFUT(self, registry, name):
        return registry.get(name)

    def test_get_existing_cookie(self):
        result = self._callFUT(self.registry, 'cookie')
        self.assertEqual(result, self.cookie_value)

    def test_get_non_existing_cookie(self):
        result = self._callFUT(self.registry, 'non_existing_cookie')
        self.assertIsNone(result)

    def test_get_with_registry(self):
        self._callFUT(self.registry)
        current = manager.get()
        self.assertEqual(current['registry'], self.registry)

    def test_get_with_empty_registry(self):
        empty_registry = Registry()
        result = self._callFUT(empty_registry, 'cookie')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()