import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne(None)

    def _makeOne(self, *args, **kwargs):
        return self.policy

    def test_get_environ_with_no_arguments(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_empty_string_key(self):
        environ = self.policy._getEnviron('', 'value')
        self.assertEqual(environ, {'': 'value'})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(key1=None)
        self.assertEqual(environ, {'key1': None})

    def test_get_environ_with_mixed_types(self):
        environ = self.policy._getEnviron(key1='value1', key2=123, key3=None)
        self.assertEqual(environ, {'key1': 'value1', 'key2': 123, 'key3': None})

    def test_get_environ_with_special_characters(self):
        environ = self.policy._getEnviron(key1='value@#$', key2='value&*()')
        self.assertEqual(environ, {'key1': 'value@#$', 'key2': 'value&*()'})