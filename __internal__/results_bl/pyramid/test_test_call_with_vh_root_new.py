import unittest
from pyramid.testing import cleanUp
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.obj = SomeClass()  # Replace with the actual class containing _getEnviron

    def tearDown(self):
        cleanUp()

    def test_empty_environ(self):
        environ = self.obj._getEnviron()
        self.assertEqual(environ, {})

    def test_single_key_value(self):
        environ = self.obj._getEnviron(HTTP_X_VHM_ROOT='/foo/bar')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar'})

    def test_multiple_key_value_pairs(self):
        environ = self.obj._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', HTTP_X_ANOTHER_HEADER='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo/bar', 'HTTP_X_ANOTHER_HEADER': 'value'})

    def test_overwrite_existing_key(self):
        environ = self.obj._getEnviron(HTTP_X_VHM_ROOT='/foo/bar', HTTP_X_VHM_ROOT='/new/path')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/new/path'})

    def test_non_string_key(self):
        with self.assertRaises(TypeError):
            self.obj._getEnviron(123='value')

    def test_non_string_value(self):
        environ = self.obj._getEnviron(HTTP_X_VHM_ROOT=123)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 123})