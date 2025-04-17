import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda environ: environ

    def test_get_environ_empty(self):
        environ = self.policy()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self.policy(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_key_value(self):
        environ = self.policy(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_overwriting_key(self):
        environ = self.policy(key1='value1', key1='value2')
        self.assertEqual(environ, {'key1': 'value2'})

    def test_get_environ_with_non_string_key(self):
        environ = self.policy(123='value')
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        environ = self.policy(key1=123)
        self.assertEqual(environ, {'key1': 123})

    def test_get_environ_with_none_value(self):
        environ = self.policy(key1=None)
        self.assertEqual(environ, {'key1': None})