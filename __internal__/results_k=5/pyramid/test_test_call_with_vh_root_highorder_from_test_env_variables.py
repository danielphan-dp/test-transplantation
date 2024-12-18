import unittest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.kwargs = {
            'HTTP_X_VHM_ROOT': 'test_root',
            'HTTP_X_VHM_OTHER': 'test_other'
        }

    def test_get_environ_with_multiple_keys(self):
        environ = self._getEnviron(**self.kwargs)
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], 'test_root')
        self.assertEqual(environ['HTTP_X_VHM_OTHER'], 'test_other')

    def test_get_environ_with_single_key(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='single_root')
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], 'single_root')
        self.assertNotIn('HTTP_X_VHM_OTHER', environ)

    def test_get_environ_with_no_keys(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_non_string_key(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT=123)
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], 123)

    def test_get_environ_overwriting_keys(self):
        environ = self._getEnviron(HTTP_X_VHM_ROOT='initial', HTTP_X_VHM_ROOT='overwritten')
        self.assertEqual(environ['HTTP_X_VHM_ROOT'], 'overwritten')

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()