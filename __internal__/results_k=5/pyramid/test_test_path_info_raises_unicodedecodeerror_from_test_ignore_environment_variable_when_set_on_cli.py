import unittest
from pyramid.exceptions import URLDecodeError
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda request: request.environ

    def test_get_environ_with_no_arguments(self):
        environ = self.policy(DummyRequest())
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.policy(DummyRequest(**{'key1': 'value1'}))
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.policy(DummyRequest(**{'key1': 'value1', 'key2': 'value2'}))
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_unicode_key(self):
        environ = self.policy(DummyRequest(**{u'key\u1234': 'value'}))
        self.assertEqual(environ, {u'key\u1234': 'value'})

    def test_get_environ_with_empty_string_key(self):
        environ = self.policy(DummyRequest(**{'': 'empty_key_value'}))
        self.assertEqual(environ, {'': 'empty_key_value'})

    def test_get_environ_with_none_value(self):
        environ = self.policy(DummyRequest(**{'key1': None}))
        self.assertEqual(environ, {'key1': None})

    def test_get_environ_with_mixed_types(self):
        environ = self.policy(DummyRequest(**{'key1': 'value1', 'key2': 123, 'key3': None}))
        self.assertEqual(environ, {'key1': 'value1', 'key2': 123, 'key3': None})

    def test_get_environ_raises_url_decode_error(self):
        toraise = UnicodeDecodeError('ascii', b'a', 2, 3, '5')
        request = DummyRequest({'key': 'value'}, toraise=toraise)
        self.assertRaises(URLDecodeError, self.policy, request)