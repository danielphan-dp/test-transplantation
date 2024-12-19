import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = 'test_cookie_value'

    def test_get_method_returns_cookie(self):
        result = self.instance.get('some_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_different_name(self):
        self.instance.cookie = 'another_cookie_value'
        result = self.instance.get('another_name')
        self.assertEqual(result, 'another_cookie_value')

    def test_get_method_with_empty_name(self):
        result = self.instance.get('')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_method_with_none_name(self):
        result = self.instance.get(None)
        self.assertEqual(result, 'test_cookie_value')

if __name__ == '__main__':
    unittest.main()