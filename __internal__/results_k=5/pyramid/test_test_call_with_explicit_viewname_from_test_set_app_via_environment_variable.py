import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.kwargs = {'key1': 'value1', 'key2': 'value2'}

    def test_get_environ_with_no_arguments(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self._getEnviron(**self.kwargs)
        self.assertEqual(environ, self.kwargs)

    def test_get_environ_with_overriding_arguments(self):
        environ = self._getEnviron(key1='new_value', key2='value2')
        self.assertEqual(environ, {'key1': 'new_value', 'key2': 'value2'})

    def test_get_environ_with_empty_arguments(self):
        environ = self._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_none_value(self):
        environ = self._getEnviron(key1=None)
        self.assertEqual(environ, {'key1': None})

    def test_get_environ_with_numeric_value(self):
        environ = self._getEnviron(key1=123)
        self.assertEqual(environ, {'key1': 123})

    def test_get_environ_with_boolean_value(self):
        environ = self._getEnviron(key1=True)
        self.assertEqual(environ, {'key1': True})

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()