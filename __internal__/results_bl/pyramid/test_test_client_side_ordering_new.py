import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation

    def test_get_method_with_valid_name(self):
        self.instance.cookie = 'test_cookie_value'
        result = self.instance.get('valid_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_empty_name(self):
        self.instance.cookie = 'test_cookie_value'
        result = self.instance.get('')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_none_name(self):
        self.instance.cookie = 'test_cookie_value'
        result = self.instance.get(None)
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_different_cookie_value(self):
        self.instance.cookie = 'another_cookie_value'
        result = self.instance.get('any_name')
        self.assertEqual(result, 'another_cookie_value')

    def test_get_method_with_unset_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('any_name')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()