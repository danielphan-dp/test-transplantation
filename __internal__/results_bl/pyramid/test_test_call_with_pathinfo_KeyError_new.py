import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne(None)

    def _makeOne(self, *args, **kwargs):
        return self.policy

    def test_get_environ_empty(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key(self):
        environ = self.policy._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_keys(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(key1=None)
        self.assertEqual(environ, {'key1': None})

    def test_get_environ_with_empty_string(self):
        environ = self.policy._getEnviron(key1='')
        self.assertEqual(environ, {'key1': ''})

    def test_get_environ_with_numeric_key(self):
        environ = self.policy._getEnviron(123='value')
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_boolean_key(self):
        environ = self.policy._getEnviron(True='value')
        self.assertEqual(environ, {True: 'value'})

    def test_get_environ_with_mixed_types(self):
        environ = self.policy._getEnviron(key1='value1', key2=2, key3=True)
        self.assertEqual(environ, {'key1': 'value1', 'key2': 2, 'key3': True})