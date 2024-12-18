import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def test_get_environ_with_single_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar/baz')
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], '/foo/bar/baz')

    def test_get_environ_with_multiple_key_values(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar/baz', SERVER_NAME='example.com', SERVER_PORT='80')
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], '/foo/bar/baz')
        self.assertEqual(environ['SERVER_NAME'], 'example.com')
        self.assertEqual(environ['SERVER_PORT'], '80')

    def test_get_environ_with_no_arguments(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_empty_string_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='')
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], '')

    def test_get_environ_with_none_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertIsNone(environ['HTTP_X_VHM_ROOT'])