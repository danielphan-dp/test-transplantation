import unittest
from pyramid.util.text_ import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.instance = DummyContext()

    def test_get_environ_empty(self):
        result = self.instance._getEnviron()
        self.assertEqual(result, {})

    def test_get_environ_single_key_value(self):
        result = self.instance._getEnviron(key='value')
        self.assertEqual(result, {'key': 'value'})

    def test_get_environ_multiple_key_value(self):
        result = self.instance._getEnviron(key1='value1', key2='value2')
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_overwrite_key(self):
        result = self.instance._getEnviron(key='initial', key='overwritten')
        self.assertEqual(result, {'key': 'overwritten'})

    def test_get_environ_with_non_string_key(self):
        result = self.instance._getEnviron(**{123: 'value'})
        self.assertEqual(result, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        result = self.instance._getEnviron(key=None)
        self.assertEqual(result, {'key': None})

    def test_get_environ_with_special_characters(self):
        result = self.instance._getEnviron(key='value with spaces & special chars!@#')
        self.assertEqual(result, {'key': 'value with spaces & special chars!@#'})