import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.helper = DummyCookies('test_cookie_value')

    def test_get_existing_cookie(self):
        self.request.cookies = {'test_cookie': 'test_cookie_value'}
        result = self.helper.get('test_cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.helper.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.request.cookies = {'empty_cookie': ''}
        result = self.helper.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_with_special_characters(self):
        self.request.cookies = {'special_cookie': 'Hällo Wörld'}
        result = self.helper.get('special_cookie')
        self.assertEqual(result, 'Hällo Wörld')

    def test_get_with_unicode_characters(self):
        self.request.cookies = {'unicode_cookie': '😊'}
        result = self.helper.get('unicode_cookie')
        self.assertEqual(result, '😊')