import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspector
from pyramid.registry import Introspectable

class TestRegistryMethods(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_get_existing_cookie(self):
        inst = self.registry
        inst.cookie = 'test_cookie'
        result = inst.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_non_existing_cookie(self):
        inst = self.registry
        result = inst.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        inst = self.registry
        inst.cookie = None
        result = inst.get('cookie')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        inst = self.registry
        inst.cookie = 'another_cookie'
        result = inst.get('different_name')
        self.assertEqual(result, 'another_cookie')