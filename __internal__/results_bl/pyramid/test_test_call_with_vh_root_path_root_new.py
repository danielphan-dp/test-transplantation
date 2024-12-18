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
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/test')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/test'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='/', USER='test_user')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/', 'USER': 'test_user'})

    def test_get_environ_with_empty_string(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': ''})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def test_get_environ_with_special_characters(self):
        environ = self.policy._getEnviron(HTTP_X_VHM_ROOT='!@#$%^&*()')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '!@#$%^&*()'})