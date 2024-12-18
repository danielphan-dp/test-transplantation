import unittest
from pyramid.testing import DummyRequest

class TestGetEnviron(unittest.TestCase):
    def setUp(self):
        self.instance = DummyContext()

    def test_get_environ_with_no_arguments(self):
        environ = self.instance._getEnviron()
        self.assertEqual(environ, {})

    def test_get_environ_with_single_argument(self):
        environ = self.instance._getEnviron(key1='value1')
        self.assertEqual(environ, {'key1': 'value1'})

    def test_get_environ_with_multiple_arguments(self):
        environ = self.instance._getEnviron(key1='value1', key2='value2')
        self.assertEqual(environ, {'key1': 'value1', 'key2': 'value2'})

    def test_get_environ_with_overwriting_key(self):
        environ = self.instance._getEnviron(key1='value1', key1='value2')
        self.assertEqual(environ, {'key1': 'value2'})

    def test_get_environ_with_empty_key(self):
        environ = self.instance._getEnviron(key1='', key2='value2')
        self.assertEqual(environ, {'key1': '', 'key2': 'value2'})

    def test_get_environ_with_none_value(self):
        environ = self.instance._getEnviron(key1=None)
        self.assertEqual(environ, {'key1': None})