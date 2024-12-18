import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'test_value'}

    def test_get_existing_cookie(self):
        result = self.request.get('test_cookie')
        self.assertEqual(result, 'test_value')

    def test_get_non_existing_cookie(self):
        result = self.request.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.get('any_cookie')
        self.assertIsNone(result)

    def test_get_with_different_cookie_name(self):
        self.request.cookies = {'another_cookie': 'another_value'}
        result = self.request.get('another_cookie')
        self.assertEqual(result, 'another_value')

    def test_get_with_special_characters_in_cookie(self):
        self.request.cookies = {'special_cookie!@#': 'special_value'}
        result = self.request.get('special_cookie!@#')
        self.assertEqual(result, 'special_value')