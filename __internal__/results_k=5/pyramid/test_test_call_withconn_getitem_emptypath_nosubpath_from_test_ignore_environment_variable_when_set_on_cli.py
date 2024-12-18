import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda **kw: self._getEnviron(**kw)

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

    def test_get_environ_empty(self):
        environ = self.policy()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key(self):
        environ = self.policy(SERVER_NAME='example.com')
        self.assertEqual(environ, {'SERVER_NAME': 'example.com'})

    def test_get_environ_with_multiple_keys(self):
        environ = self.policy(SERVER_NAME='example.com', SERVER_PORT='80')
        self.assertEqual(environ, {'SERVER_NAME': 'example.com', 'SERVER_PORT': '80'})

    def test_get_environ_with_conflicting_keys(self):
        environ = self.policy(SERVER_NAME='example.com', SERVER_NAME='test.com')
        self.assertEqual(environ, {'SERVER_NAME': 'test.com'})

    def test_get_environ_with_none_value(self):
        environ = self.policy(SERVER_NAME=None)
        self.assertEqual(environ, {'SERVER_NAME': None})

    def test_get_environ_with_empty_string(self):
        environ = self.policy(SERVER_NAME='')
        self.assertEqual(environ, {'SERVER_NAME': ''})