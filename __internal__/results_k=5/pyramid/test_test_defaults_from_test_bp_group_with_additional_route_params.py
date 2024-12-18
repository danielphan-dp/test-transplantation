import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'cookie_value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test_cookie')
        self.assertEqual(result, 'cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {}
        result = self.request.cookies.get('empty_cookie')
        self.assertIsNone(result)

    def test_get_with_special_characters(self):
        self.request.cookies = {'special_cookie!@#': 'special_value'}
        result = self.request.cookies.get('special_cookie!@#')
        self.assertEqual(result, 'special_value')

    def test_get_cookie_with_none(self):
        self.request.cookies = {'none_cookie': None}
        result = self.request.cookies.get('none_cookie')
        self.assertIsNone(result)