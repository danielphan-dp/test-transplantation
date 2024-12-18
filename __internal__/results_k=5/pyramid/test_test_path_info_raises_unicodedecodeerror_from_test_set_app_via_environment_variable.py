import unittest
from pyramid.exceptions import URLDecodeError
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda request: request.environ

    def test_get_environ_empty(self):
        environ = self.policy(DummyRequest())
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self.policy(DummyRequest({'key': 'value'}))
        self.assertEqual(environ, {'key': 'value'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self.policy(DummyRequest({'key1': 'value1', 'key2': 'value2'}))
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_unicode_key_value(self):
        environ = self.policy(DummyRequest({'key': 'value', 'unicode_key': '测试'}))
        self.assertEqual(environ, {'key': 'value', 'unicode_key': '测试'})

    def test_get_environ_with_none_value(self):
        environ = self.policy(DummyRequest({'key': None}))
        self.assertEqual(environ, {'key': None})

    def test_get_environ_raises_url_decode_error(self):
        toraise = UnicodeDecodeError('ascii', b'a', 2, 3, '5')
        request = DummyRequest({'key': 'value'}, toraise=toraise)
        self.assertRaises(URLDecodeError, self.policy, request)