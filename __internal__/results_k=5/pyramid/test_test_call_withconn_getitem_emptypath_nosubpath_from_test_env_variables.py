import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        return lambda environ: environ

    def test_get_environ_empty(self):
        environ = self.policy()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_key_value(self):
        environ = self.policy(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_key_value(self):
        environ = self.policy(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_none_value(self):
        environ = self.policy(key1=None)
        self.assertEqual(environ, {'key1': None})

    def test_get_environ_with_empty_string_value(self):
        environ = self.policy(key1='')
        self.assertEqual(environ, {'key1': ''})

    def test_get_environ_with_boolean_value(self):
        environ = self.policy(key1=True, key2=False)
        self.assertEqual(environ, {'key1': True, 'key2': False})

    def test_get_environ_with_nested_dict(self):
        environ = self.policy(key1={'nested_key': 'nested_value'})
        self.assertEqual(environ, {'key1': {'nested_key': 'nested_value'}})

    def test_get_environ_with_list_value(self):
        environ = self.policy(key1=['value1', 'value2'])
        self.assertEqual(environ, {'key1': ['value1', 'value2']})

if __name__ == '__main__':
    unittest.main()