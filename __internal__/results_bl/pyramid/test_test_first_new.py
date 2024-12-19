import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = b'OK'  # Set up the cookie attribute

    def test_get_existing_cookie(self):
        result = self.instance.get('some_name')
        self.assertEqual(result, b'OK')

    def test_get_empty_cookie(self):
        self.instance.cookie = b''  # Set cookie to empty
        result = self.instance.get('some_name')
        self.assertEqual(result, b'')

    def test_get_none_cookie(self):
        self.instance.cookie = None  # Set cookie to None
        result = self.instance.get('some_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.instance.cookie = b'AnotherValue'  # Change cookie value
        result = self.instance.get('different_name')
        self.assertEqual(result, b'AnotherValue')

if __name__ == '__main__':
    unittest.main()