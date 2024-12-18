import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.system = {}
        self.event = self._makeOne(self.system)

    def _makeOne(self, system):
        class Event:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        return Event(None)

    def test_get_none(self):
        self.assertEqual(self.event.get('a'), None)

    def test_get_with_cookie(self):
        self.event = self._makeOne('test_cookie_value')
        self.assertEqual(self.event.get('a'), 'test_cookie_value')

    def test_get_empty_cookie(self):
        self.event = self._makeOne('')
        self.assertEqual(self.event.get('a'), '')