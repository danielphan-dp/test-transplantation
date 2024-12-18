import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = DummyPolicy()

    def test_get_environ_with_no_arguments(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy._getEnviron(foo='bar')
        self.assertEqual(environ, {'foo': 'bar'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy._getEnviron(foo='bar', baz='qux')
        self.assertEqual(environ, {'foo': 'bar', 'baz': 'qux'})

    def test_get_environ_with_overlapping_keys(self):
        environ = self.policy._getEnviron(foo='bar', foo='baz')
        self.assertEqual(environ, {'foo': 'baz'})

    def test_get_environ_with_non_string_keys(self):
        environ = self.policy._getEnviron(**{1: 'one', 2: 'two'})
        self.assertEqual(environ, {1: 'one', 2: 'two'})

class DummyPolicy:
    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()