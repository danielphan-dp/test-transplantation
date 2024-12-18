import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.system = {'a': 1, 'b': 2}
        self.event = self._makeOne(self.system)

    def _makeOne(self, system):
        class DummyEvent:
            def __init__(self, system):
                self.system = system

            def get(self, name):
                return self.system.get(name)

        return DummyEvent(system)

    def test_get_existing_key(self):
        self.assertEqual(self.event.get('a'), 1)

    def test_get_non_existing_key(self):
        self.assertIsNone(self.event.get('c'))

    def test_get_another_existing_key(self):
        self.assertEqual(self.event.get('b'), 2)

    def test_get_with_empty_system(self):
        empty_event = self._makeOne({})
        self.assertIsNone(empty_event.get('a'))