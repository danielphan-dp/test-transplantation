import unittest
from pyramid.exceptions import URLDecodeError

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.policy = DummyPolicy()  # Assuming DummyPolicy is defined elsewhere

    def test_get_environ_empty(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key(self):
        environ = self.policy._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_keys(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_overwrite_key(self):
        environ = self.policy._getEnviron(key1='value1', key1='value2')
        self.assertEqual(environ, {'key1': 'value2'})

    def test_get_environ_with_non_string_key(self):
        environ = self.policy._getEnviron(123='value')
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        environ = self.policy._getEnviron(key1=123)
        self.assertEqual(environ, {'key1': 123})

    def test_get_environ_with_unicode_key_value(self):
        environ = self.policy._getEnviron(key1='value1', key2='测试')
        self.assertEqual(environ, {'key1': 'value1', 'key2': '测试'})