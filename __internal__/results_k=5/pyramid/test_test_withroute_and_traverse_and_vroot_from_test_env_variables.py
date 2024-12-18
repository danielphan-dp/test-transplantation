import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.instance = DummyContext()

    def test_get_environ_with_single_key_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/abc')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/abc'})

    def test_get_environ_with_multiple_key_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/abc', ANOTHER_KEY='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/abc', 'ANOTHER_KEY': 'value'})

    def test_get_environ_with_no_arguments(self):
        environ = self.instance._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_empty_string_key(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': ''})

    def test_get_environ_with_none_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})