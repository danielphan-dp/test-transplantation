import unittest
from pyramid.testing import DummyRequest
from your_module import YourClass  # Replace with the actual module and class name

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.instance = YourClass()  # Replace with the actual class instantiation

    def test_get_method_returns_cookie(self):
        self.instance.cookie = 'test_cookie'
        result = self.instance.get('test_name')
        self.assertEqual(result, 'test_cookie')

    def test_get_method_with_no_cookie(self):
        self.instance.cookie = None
        result = self.instance.get('test_name')
        self.assertIsNone(result)

    def test_get_method_with_empty_string(self):
        self.instance.cookie = ''
        result = self.instance.get('test_name')
        self.assertEqual(result, '')

    def test_get_method_with_different_name(self):
        self.instance.cookie = 'another_cookie'
        result = self.instance.get('different_name')
        self.assertEqual(result, 'another_cookie')