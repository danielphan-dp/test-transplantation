import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = 'test_cookie_value'  # Set a default cookie value

    def test_get_existing_cookie(self):
        result = self.instance.get('some_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_empty_cookie(self):
        self.instance.cookie = ''
        result = self.instance.get('some_name')
        self.assertEqual(result, '')

    def test_get_none_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('some_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.instance.cookie = 'another_cookie_value'
        result = self.instance.get('different_name')
        self.assertEqual(result, 'another_cookie_value')

if __name__ == '__main__':
    unittest.main()