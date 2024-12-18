import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne(DummyContext())

    def _makeOne(self, root):
        return lambda request: {
            'context': root,
            'view_name': '',
            'subpath': (),
            'traversed': (),
            'root': root,
            'virtual_root': root,
            'virtual_root_path': ()
        }

    def test_get_environ_with_no_arguments(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy._getEnviron(key='value')
        self.assertEqual(environ, {'key': 'value'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_empty_string_key(self):
        environ = self.policy._getEnviron(key='', value='test')
        self.assertEqual(environ, {'key': '', 'value': 'test'})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(key=None)
        self.assertEqual(environ, {'key': None})

    def test_get_environ_with_numeric_key(self):
        environ = self.policy._getEnviron(123='numeric')
        self.assertEqual(environ, {123: 'numeric'})