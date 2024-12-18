import unittest
from pyramid.testing import DummyRequest

class TestEventGetMethod(unittest.TestCase):

    def _makeOne(self, system):
        return DummyRequest(system)

    def test_get_existing_cookie(self):
        system = {'cookie': 'test_cookie'}
        event = self._makeOne(system)
        self.assertEqual(event.get('cookie'), 'test_cookie')

    def test_get_non_existing_cookie(self):
        system = {}
        event = self._makeOne(system)
        self.assertEqual(event.get('non_existing_cookie'), None)

    def test_get_empty_cookie(self):
        system = {'cookie': ''}
        event = self._makeOne(system)
        self.assertEqual(event.get('cookie'), '')

    def test_get_with_special_characters(self):
        system = {'cookie': 'cookie_with_special_chars!@#$%^&*()'}
        event = self._makeOne(system)
        self.assertEqual(event.get('cookie'), 'cookie_with_special_chars!@#$%^&*()')