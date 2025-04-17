import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.instance = DummyContext()

    def test_get_environ_empty(self):
        result = self.instance._getEnviron()
        self.assertEqual(result, {})

    def test_get_environ_with_single_key_value(self):
        result = self.instance._getEnviron(key1='value1')
        self.assertEqual(result, {'key1': 'value1'})

    def test_get_environ_with_multiple_key_values(self):
        result = self.instance._getEnviron(key1='value1', key2='value2')
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_overwrite_key(self):
        result = self.instance._getEnviron(key1='value1', key1='value2')
        self.assertEqual(result, {'key1': 'value2'})

    def test_get_environ_with_non_string_keys(self):
        result = self.instance._getEnviron(1='value1', 2='value2')
        self.assertEqual(result, {1: 'value1', 2: 'value2'})

    def test_get_environ_with_none_value(self):
        result = self.instance._getEnviron(key1=None)
        self.assertEqual(result, {'key1': None})