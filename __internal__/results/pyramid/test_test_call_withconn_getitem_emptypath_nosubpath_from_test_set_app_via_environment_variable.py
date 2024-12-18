import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda environ: environ

    def test_get_environ_with_no_arguments(self):
        environ = self.policy()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy(key='value')
        self.assertEqual(environ, {'key': 'value'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_empty_string_key(self):
        environ = self.policy('', 'value')
        self.assertEqual(environ, {'': 'value'})

    def test_get_environ_with_none_value(self):
        environ = self.policy(key=None)
        self.assertEqual(environ, {'key': None})

    def test_get_environ_with_boolean_value(self):
        environ = self.policy(key=True)
        self.assertEqual(environ, {'key': True})

    def test_get_environ_with_numeric_value(self):
        environ = self.policy(key=123)
        self.assertEqual(environ, {'key': 123})

    def test_get_environ_with_mixed_types(self):
        environ = self.policy(key1='value1', key2=123, key3=None, key4=True)
        self.assertEqual(environ, {'key1': 'value1', 'key2': 123, 'key3': None, 'key4': True})