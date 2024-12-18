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

    def test_get_environ_with_unicode(self):
        path = text_(b'Qu\xc3\xa9bec', 'utf-8')
        environ = self._getEnviron(HTTP_X_VHM_ROOT=path)
        self.assertEqual(environ, {'HTTP_X_VHM_ROOT': path})

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()