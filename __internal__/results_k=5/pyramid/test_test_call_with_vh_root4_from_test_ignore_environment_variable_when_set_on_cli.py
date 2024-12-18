import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def test_get_environ_with_single_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar/baz')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar/baz'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar/baz', ANOTHER_KEY='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar/baz', 'ANOTHER_KEY': 'value'})

    def test_get_environ_with_no_arguments(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_empty_string_key_value(self):
        environ = self._getEnviron(EMPTY_KEY='')
        self.assertEqual(environ, {'EMPTY_KEY': ''})

    def test_get_environ_with_none_value(self):
        environ = self._getEnviron(NONE_KEY=None)
        self.assertEqual(environ, {'NONE_KEY': None})