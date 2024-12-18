import unittest
from pyramid.registry import Registry
from pyramid.threadlocal import get_current_registry, manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.request = DummyRequest()
        self.cookie = 'test_cookie'
        self.config = self._callFUT()

    def _callFUT(self):
        return self.registry

    def test_get_returns_cookie(self):
        self.config.cookie = self.cookie
        result = self.config.get('test_name')
        self.assertEqual(result, self.cookie)

    def test_get_with_no_cookie(self):
        self.config.cookie = None
        result = self.config.get('test_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.config.cookie = 'another_cookie'
        result = self.config.get('different_name')
        self.assertEqual(result, 'another_cookie')

    def test_get_with_empty_name(self):
        self.config.cookie = 'empty_name_cookie'
        result = self.config.get('')
        self.assertEqual(result, 'empty_name_cookie')

    def test_get_with_nonexistent_name(self):
        self.config.cookie = 'nonexistent_cookie'
        result = self.config.get('nonexistent_name')
        self.assertEqual(result, 'nonexistent_cookie')

if __name__ == '__main__':
    unittest.main()