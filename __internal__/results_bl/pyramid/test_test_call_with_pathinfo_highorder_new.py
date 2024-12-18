import unittest
from pyramid.util.text_ import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = DummyPolicy()

    def test_get_environ_empty(self):
        environ = self.policy._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self.policy._getEnviron(key='value')
        self.assertEqual(environ, {'key': 'value'})

    def test_get_environ_with_multiple_key_values(self):
        environ = self.policy._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_non_string_key(self):
        environ = self.policy._getEnviron(**{123: 'value'})
        self.assertEqual(environ, {123: 'value'})

    def test_get_environ_with_non_string_value(self):
        environ = self.policy._getEnviron(key='value', another_key=123)
        self.assertEqual(environ, {'key': 'value', 'another_key': 123})

    def test_get_environ_with_none_value(self):
        environ = self.policy._getEnviron(key=None)
        self.assertEqual(environ, {'key': None})

class DummyPolicy:
    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()