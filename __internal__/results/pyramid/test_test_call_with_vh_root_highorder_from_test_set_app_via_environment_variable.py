import unittest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.kw = {'HTTP_X_VHM_ROOT': 'test_root'}

    def test_get_environ_with_default(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='test_root')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'test_root'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='test_root', ANOTHER_KEY='another_value')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 'test_root', 'ANOTHER_KEY': 'another_value'})

    def test_get_environ_with_non_string_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=12345)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': 12345})

    def test_get_environ_with_empty_key_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='')
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': ''})

    def test_get_environ_with_none_value(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=None)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': None})

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()