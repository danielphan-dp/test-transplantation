import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def _makeOne(self, cookie=None):
        class DummyEvent:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        return DummyEvent(cookie)

    def test_get_with_none_cookie(self):
        event = self._makeOne(None)
        self.assertIsNone(event.get('a'))

    def test_get_with_empty_cookie(self):
        event = self._makeOne('')
        self.assertEqual(event.get('a'), '')

    def test_get_with_valid_cookie(self):
        event = self._makeOne('valid_cookie_value')
        self.assertEqual(event.get('a'), 'valid_cookie_value')

    def test_get_with_different_cookie_name(self):
        event = self._makeOne('another_cookie_value')
        self.assertEqual(event.get('b'), 'another_cookie_value')

    def test_get_with_nonexistent_cookie(self):
        event = self._makeOne('some_cookie_value')
        self.assertIsNone(event.get('nonexistent_cookie'))