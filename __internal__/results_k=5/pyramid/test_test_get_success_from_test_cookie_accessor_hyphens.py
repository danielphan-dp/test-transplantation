import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.system = {'a': 1, 'b': 2}
        self.event = self._makeOne(self.system)

    def _makeOne(self, system):
        class DummyEvent:
            def __init__(self, system):
                self.cookie = system

            def get(self, name):
                return self.cookie.get(name)

        return DummyEvent(system)

    def test_get_existing_key(self):
        self.assertEqual(self.event.get('a'), 1)

    def test_get_non_existing_key(self):
        self.assertIsNone(self.event.get('c'))

    def test_get_another_existing_key(self):
        self.assertEqual(self.event.get('b'), 2)

    def test_get_with_hyphen(self):
        self.event.cookie = {'session-token': 'abc123'}
        self.assertEqual(self.event.get('session-token'), 'abc123')

    def test_get_empty_cookie(self):
        self.event.cookie = {}
        self.assertIsNone(self.event.get('a'))