import unittest
from pyramid import testing

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.request = DummyRequest()
        self.policy = self._makeOne()

    def _makeOne(self):
        return DummyCookieHelper('test_cookie_value')

    def test_get_existing_cookie(self):
        result = self.policy.get('test_cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.policy.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.policy = self._makeOne('')
        result = self.policy.get('empty_cookie')
        self.assertEqual(result, '')

    def test_get_with_special_characters(self):
        self.policy = self._makeOne('cookie_with_special_chars_!@#$%^&*()')
        result = self.policy.get('special_char_cookie')
        self.assertEqual(result, 'cookie_with_special_chars_!@#$%^&*()')