import unittest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.instance = DummyClass()  # Replace with actual class that contains _getEnviron

    def test_get_environ_with_single_key_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='test_root')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'test_root'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='test_root', ANOTHER_KEY='another_value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'test_root', 'ANOTHER_KEY': 'another_value'})

    def test_get_environ_with_empty(self):
        environ = self.instance._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_non_string_key(self):
        environ = self.instance._getEnviron(**{123: 'value'})
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT=123)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 123})

    def test_get_environ_with_special_characters(self):
        special_value = text_(b'Qu\xc3\xa9bec', 'utf-8')
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT=special_value)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': special_value})