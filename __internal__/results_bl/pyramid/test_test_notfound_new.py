import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation
        self.instance.cookie = 'test_cookie_value'

    def test_get_existing_cookie(self):
        result = self.instance.get('test_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_empty_cookie(self):
        self.instance.cookie = ''
        result = self.instance.get('test_name')
        self.assertEqual(result, '')

    def test_get_none_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('test_name')
        self.assertIsNone(result)

    def test_get_with_different_name(self):
        result = self.instance.get('another_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_unset_cookie(self):
        self.instance.cookie = 'unset_value'
        result = self.instance.get('test_name')
        self.assertEqual(result, 'unset_value')

if __name__ == '__main__':
    unittest.main()