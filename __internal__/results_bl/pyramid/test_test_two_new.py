import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = b'Test Cookie'  # Set a default cookie value

    def test_get_existing_cookie(self):
        result = self.instance.get('some_name')
        self.assertEqual(result, b'Test Cookie')

    def test_get_empty_cookie(self):
        self.instance.cookie = b''  # Set cookie to empty
        result = self.instance.get('some_name')
        self.assertEqual(result, b'')

    def test_get_none_cookie(self):
        self.instance.cookie = None  # Set cookie to None
        result = self.instance.get('some_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        self.instance.cookie = b'Another Cookie'  # Change cookie value
        result = self.instance.get('different_name')
        self.assertEqual(result, b'Another Cookie')

if __name__ == '__main__':
    unittest.main()