import unittest
from pyramid.registry import Registry
from pyramid.interfaces import IIntrospector
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspector = IIntrospector(self.registry)
        self.introspectable = Introspectable('category', 'discriminator_hash', self.introspector)

    def _makeOne(self):
        return self.registry

    def test_get_success(self):
        inst = self._makeOne()
        inst.add(self.introspectable)
        result = inst.get('category', 'discriminator_hash')
        self.assertEqual(result, self.introspectable)

    def test_get_non_existent(self):
        inst = self._makeOne()
        result = inst.get('non_existent_category', 'non_existent_discriminator')
        self.assertIsNone(result)

    def test_get_with_empty_registry(self):
        inst = self._makeOne()
        result = inst.get('empty_category', 'empty_discriminator')
        self.assertIsNone(result)

    def test_get_with_invalid_arguments(self):
        inst = self._makeOne()
        with self.assertRaises(TypeError):
            inst.get(None)

    def test_get_with_different_discriminator(self):
        inst = self._makeOne()
        intr2 = Introspectable('category', 'different_discriminator', self.introspector)
        inst.add(intr2)
        result = inst.get('category', 'different_discriminator')
        self.assertEqual(result, intr2)