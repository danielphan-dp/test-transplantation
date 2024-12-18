import unittest
from pyramid.testing import cleanUp
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.kwargs = {}

    def tearDown(self):
        cleanUp()

    def test_empty_environ(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_single_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/foo')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/foo'})

    def test_multiple_key_value_pairs(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/', HTTP_X_ANOTHER_HEADER='value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/', 'HTTP_X_ANOTHER_HEADER': 'value'})

    def test_overwrite_key(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='/', HTTP_X_VHM_ROOT='/bar')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': '/bar'})

    def test_non_string_key(self):
        with self.assertRaises(TypeError):
            self._getEnviron(HTTP_X_VHM_ROOT=123)

    def test_non_string_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def test_special_characters_in_key(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='value_with_special_chars_!@#$%^&*()')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'value_with_special_chars_!@#$%^&*()'})

    def test_special_characters_in_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='value_with_special_chars_!@#$%^&*()')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'value_with_special_chars_!@#$%^&*()'})