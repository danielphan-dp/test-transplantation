import unittest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class name that contains _getEnviron

    def test_empty_environ(self):
        environ = self.instance._getEnviron()
        self.assertEqual(environ, {})

    def test_single_key_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/foo/bar')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar'})

    def test_multiple_key_value_pairs(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', ANOTHER_KEY='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar', 'ANOTHER_KEY': 'value'})

    def test_overwrite_existing_key(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', HTTP_X_VHM_ROOT='/new/path')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/new/path'})

    def test_non_string_key(self):
        environ = self.instance._getEnviron(**{123: 'value'})
        self.assertEqual(environ, {123: 'value'})

    def test_non_string_value(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT=123)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 123})

    def test_combined_key_value_types(self):
        environ = self.instance._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', NUMERIC_KEY=42, BOOLEAN_KEY=True)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar', 'NUMERIC_KEY': 42, 'BOOLEAN_KEY': True})