import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspectable = Introspectable()
        self.registry.add(self.introspectable)

    def test_get_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = 'test_cookie_value'
        self.assertEqual(inst.get('test_cookie_name'), 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        inst = self._makeOne()
        inst.cookie = None
        self.assertIsNone(inst.get('non_existing_cookie'))

    def test_get_with_default_value(self):
        inst = self._makeOne()
        inst.cookie = None
        self.assertEqual(inst.get('non_existing_cookie', 'default_value'), 'default_value')

    def _makeOne(self):
        return DummyCookies(None)

class DummyCookies:
    def __init__(self, cookie):
        self.cookie = cookie

    def get(self, name):
        return self.cookie