import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne(None)

    def _makeOne(self, *args, **kwargs):
        return self.policy

    def test_get_environ_with_single_key_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/', SERVER_NAME='example.com')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/', 'SERVER_NAME': 'example.com'})

    def test_get_environ_with_no_arguments(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_different_key_types(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/', CUSTOM_HEADER='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/', 'CUSTOM_HEADER': 'value'})

    def test_get_environ_with_empty_string_key(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='', EMPTY_HEADER='')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '', 'EMPTY_HEADER': ''})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def test_get_environ_with_numeric_key_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/', NUMERIC_HEADER=123)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/', 'NUMERIC_HEADER': 123})