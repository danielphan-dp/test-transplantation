import unittest
from pyramid.util import text_
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
        environ = self.policy._getEnviron(foo='bar')
        self.assertEqual(environ, {'foo': 'bar'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(foo='bar', baz='qux')
        self.assertEqual(environ, {'foo': 'bar', 'baz': 'qux'})

    def test_get_environ_with_overwriting_arguments(self):
        environ = self.policy._getEnviron(foo='bar', foo='baz')
        self.assertEqual(environ, {'foo': 'baz'})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(foo=None)
        self.assertEqual(environ, {'foo': None})

    def test_get_environ_with_empty_string_value(self):
        environ = self.policy._getEnviron(foo='')
        self.assertEqual(environ, {'foo': ''})

    def test_get_environ_with_numeric_value(self):
        environ = self.policy._getEnviron(foo=123)
        self.assertEqual(environ, {'foo': 123})

    def test_get_environ_with_boolean_value(self):
        environ = self.policy._getEnviron(foo=True)
        self.assertEqual(environ, {'foo': True})

    def test_get_environ_with_list_value(self):
        environ = self.policy._getEnviron(foo=['bar', 'baz'])
        self.assertEqual(environ, {'foo': ['bar', 'baz']})

    def test_get_environ_with_dict_value(self):
        environ = self.policy._getEnviron(foo={'key': 'value'})
        self.assertEqual(environ, {'foo': {'key': 'value'}})