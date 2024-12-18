import unittest
from pyramid.util.text_ import text_

class TestGetEnviron(unittest.TestCase):

    def setUp(self):
        self.kwargs = {'key1': 'value1', 'key2': 'value2'}

    def test_get_environ_with_no_arguments(self):
        result = self._getEnviron()
        self.assertEqual(result, {})

    def test_get_environ_with_single_argument(self):
        result = self._getEnviron(key1='value1')
        self.assertEqual(result, {'key1': 'value1'})

    def test_get_environ_with_multiple_arguments(self):
        result = self._getEnviron(**self.kwargs)
        self.assertEqual(result, self.kwargs)

    def test_get_environ_with_overriding_arguments(self):
        result = self._getEnviron(key1='new_value', key3='value3')
        self.assertEqual(result, {'key1': 'new_value', 'key3': 'value3'})

    def test_get_environ_with_empty_arguments(self):
        result = self._getEnviron()
        self.assertEqual(result, {})

    def test_get_environ_with_non_string_keys(self):
        result = self._getEnviron(**{1: 'value1', 2: 'value2'})
        self.assertEqual(result, {1: 'value1', 2: 'value2'})

    def test_get_environ_with_non_string_values(self):
        result = self._getEnviron(key1=123, key2=[1, 2, 3])
        self.assertEqual(result, {'key1': 123, 'key2': [1, 2, 3]})

    def _getEnviron(self, **kw):
        environ = {}
        environ.update(kw)
        return environ

if __name__ == '__main__':
    unittest.main()