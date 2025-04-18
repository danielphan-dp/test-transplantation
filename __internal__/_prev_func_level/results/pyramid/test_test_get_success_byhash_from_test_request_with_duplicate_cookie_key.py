import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspectable = Introspectable()
        self.registry.registerUtility(self.introspectable, name='category')

    def test_get_success(self):
        result = self.registry.get('category')
        self.assertEqual(result, self.introspectable)

    def test_get_non_existent(self):
        result = self.registry.get('non_existent')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.registry.registerUtility(self.introspectable, name='another_category')
        result = self.registry.get('another_category')
        self.assertEqual(result, self.introspectable)

    def test_get_with_empty_name(self):
        result = self.registry.get('')
        self.assertIsNone(result)

    def test_get_with_none_name(self):
        result = self.registry.get(None)
        self.assertIsNone(result)