import unittest
from pyramid.util import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.instance = DummyContext(None, 'dummy_path')

    def test_get_environ_empty(self):
        environ = self.instance._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self.instance._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_key_value(self):
        environ = self.instance._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_non_string_key(self):
        environ = self.instance._getEnviron(123='value')
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        environ = self.instance._getEnviron(key1=123)
        self.assertEqual(environ, {'key1': 123})

    def test_get_environ_with_mixed_types(self):
        environ = self.instance._getEnviron(key1='value1', key2=123, key3=None)
        self.assertEqual(environ, {'key1': 'value1', 'key2': 123, 'key3': None})

if __name__ == '__main__':
    unittest.main()