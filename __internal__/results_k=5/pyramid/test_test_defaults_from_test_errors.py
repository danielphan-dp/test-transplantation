import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'cookie_value'}

    def test_get_existing_cookie(self):
        result = self.request.get('test_cookie')
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.request.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.get('empty_cookie')
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        self.request.cookies = {'special_cookie!@#': 'special_value'}
        result = self.request.get('special_cookie!@#')
        self.assertEqual(result, 'special_value')

    def test_get_with_none_name(self):
        with self.assertRaises(TypeError):
            self.request.get(None)