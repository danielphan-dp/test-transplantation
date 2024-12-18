import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne(None)

    def _makeOne(self, *args, **kwargs):
        return self.policy

    def test_get_environ_with_no_arguments(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy._getEnviron(key='value')
        self.assertEqual(environ, {'key': 'value'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_overwriting_key(self):
        environ = self.policy._getEnviron(key='initial', key='overwritten')
        self.assertEqual(environ, {'key': 'overwritten'})

    def test_get_environ_with_non_string_keys(self):
        environ = self.policy._getEnviron(**{1: 'value1', 2: 'value2'})
        self.assertEqual(environ, {1: 'value1', 2: 'value2'})

    def test_get_environ_with_empty_key(self):
        environ = self.policy._getEnviron(**{'': 'empty_key'})
        self.assertEqual(environ, {'': 'empty_key'})