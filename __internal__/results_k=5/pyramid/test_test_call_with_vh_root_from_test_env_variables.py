import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def test_get_environ_with_single_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', SERVER_NAME='example.com', SERVER_PORT='80')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar', 'SERVER_NAME': 'example.com', 'SERVER_PORT': '80'})

    def test_get_environ_with_empty(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_none_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def test_get_environ_with_special_characters(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='foo/bar?baz=qux')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'foo/bar?baz=qux'})