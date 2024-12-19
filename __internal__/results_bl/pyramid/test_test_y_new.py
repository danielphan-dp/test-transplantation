import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.request = DummyRequest()

    def test_get_returns_cookie(self):
        expected_cookie = 'test_cookie_value'  # Replace with the expected cookie value
        self.instance.cookie = expected_cookie
        result = self.instance.get('test_name')
        self.assertEqual(result, expected_cookie)

    def test_get_with_no_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('test_name')
        self.assertIsNone(result)

    def test_get_with_empty_cookie(self):
        self.instance.cookie = ''
        result = self.instance.get('test_name')
        self.assertEqual(result, '')

    def test_get_with_different_name(self):
        self.instance.cookie = 'another_cookie_value'
        result = self.instance.get('different_name')
        self.assertEqual(result, 'another_cookie_value')

if __name__ == '__main__':
    unittest.main()