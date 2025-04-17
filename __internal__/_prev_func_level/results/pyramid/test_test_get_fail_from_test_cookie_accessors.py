import unittest
from pyramid.registry import Registry
from pyramid.interfaces import IIntrospector
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspector = IIntrospector(self.registry)

    def _makeOne(self):
        return self.introspector

    def test_get_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = 'test_cookie_value'
        self.assertEqual(inst.get('test_cookie'), 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = None
        self.assertIsNone(inst.get('non_existing_cookie'))

    def test_get_with_default_value(self):
        inst = self._makeOne()
        inst.cookie = None
        self.assertEqual(inst.get('non_existing_cookie', 'default_value'), 'default_value')

    def test_get_with_empty_string(self):
        inst = self._makeOne()
        inst.cookie = ''
        self.assertEqual(inst.get('empty_cookie'), '')

    def test_get_with_special_characters(self):
        inst = self._makeOne()
        inst.cookie = 'cookie_with_special_chars!@#$%^&*()'
        self.assertEqual(inst.get('special_cookie'), 'cookie_with_special_chars!@#$%^&*()')