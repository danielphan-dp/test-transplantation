import unittest
from pyramid.registry import Registry
from pyramid.interfaces import IIntrospector

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspector = DummyIntrospectable()
        self.registry.introspector = self.introspector

    def test_get_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = {'foo': 'bar'}
        self.assertEqual(inst.get('foo'), 'bar')

    def test_get_non_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = {}
        self.assertIsNone(inst.get('nonexistent'))

    def test_get_with_default_value(self):
        inst = self._makeOne()
        inst.cookie = {'foo': 'bar'}
        self.assertEqual(inst.get('foo', 'default'), 'bar')
        self.assertEqual(inst.get('nonexistent', 'default'), 'default')

    def test_get_empty_cookie(self):
        inst = self._makeOne()
        inst.cookie = {}
        self.assertEqual(inst.get('foo', 'default'), 'default')

    def _makeOne(self):
        class Dummy:
            def __init__(self):
                self.cookie = {}

            def get(self, name, default=None):
                return self.cookie.get(name, default)

        return Dummy()