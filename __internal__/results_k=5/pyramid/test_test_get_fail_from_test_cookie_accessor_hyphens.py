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

    def test_get_with_valid_cookie(self):
        event = self._makeOne('valid_cookie')
        self.assertEqual(event.get('cookie_name'), 'valid_cookie')

    def test_get_with_none_cookie(self):
        event = self._makeOne(None)
        self.assertEqual(event.get('cookie_name'), None)

    def test_get_with_empty_string_cookie(self):
        event = self._makeOne('')
        self.assertEqual(event.get('cookie_name'), '')

    def test_get_with_nonexistent_cookie(self):
        event = self._makeOne('some_cookie')
        self.assertEqual(event.get('nonexistent_cookie'), 'some_cookie')