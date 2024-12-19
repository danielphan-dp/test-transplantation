import unittest
from pyramid.testing import DummyRequest
from pyramid.threadlocal import get_current_request

class TestThreadLocal(unittest.TestCase):

    def setUp(self):
        self.local = self._makeOne()

    def _makeOne(self):
        return DummyRequest()

    def test_get_without_set(self):
        self.assertIsNone(self.local.get('non_existent_key'))

    def test_get_after_set(self):
        self.local.set('test_key', 'test_value')
        self.assertEqual(self.local.get('test_key'), 'test_value')

    def test_get_after_clear(self):
        self.local.set('test_key', 'test_value')
        self.local.clear()
        self.assertIsNone(self.local.get('test_key'))

    def test_get_with_none_value(self):
        self.local.set('none_key', None)
        self.assertIsNone(self.local.get('none_key'))

    def test_get_with_multiple_keys(self):
        self.local.set('key1', 'value1')
        self.local.set('key2', 'value2')
        self.assertEqual(self.local.get('key1'), 'value1')
        self.assertEqual(self.local.get('key2'), 'value2')

    def test_get_with_invalid_key(self):
        self.assertIsNone(self.local.get('invalid_key'))