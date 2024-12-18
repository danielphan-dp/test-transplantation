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

    def test_get_environ_with_empty(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def test_get_environ_with_numeric_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT=123)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 123})

    def test_get_environ_with_boolean_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT=True)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': True})

    def test_get_environ_with_special_characters(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='path/to/resource?query=1&other=2')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'path/to/resource?query=1&other=2'})