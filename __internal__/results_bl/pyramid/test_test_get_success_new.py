import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspectable = Introspectable('category', 'discriminator')

    def test_get_existing_introspectable(self):
        self.registry.add(self.introspectable)
        result = self.registry.get('category', 'discriminator')
        self.assertEqual(result, self.introspectable)

    def test_get_non_existing_introspectable(self):
        result = self.registry.get('non_existing_category', 'discriminator')
        self.assertIsNone(result)

    def test_get_with_empty_name(self):
        self.registry.add(self.introspectable)
        result = self.registry.get('')
        self.assertIsNone(result)

    def test_get_with_none_name(self):
        self.registry.add(self.introspectable)
        result = self.registry.get(None)
        self.assertIsNone(result)

    def test_get_multiple_introspectables(self):
        intr1 = Introspectable('category1', 'discriminator1')
        intr2 = Introspectable('category2', 'discriminator2')
        self.registry.add(intr1)
        self.registry.add(intr2)
        result = self.registry.get('category1', 'discriminator1')
        self.assertEqual(result, intr1)
        result = self.registry.get('category2', 'discriminator2')
        self.assertEqual(result, intr2)