import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    
    def _makeOne(self, system):
        class Event:
            def __init__(self, system):
                self.cookie = system
            
            def get(self, name):
                return self.cookie.get(name)
        
        return Event(system)

    def test_get_non_existent_key(self):
        system = {'a': 1}
        event = self._makeOne(system)
        self.assertIsNone(event.get('b'))

    def test_get_empty_system(self):
        system = {}
        event = self._makeOne(system)
        self.assertIsNone(event.get('a'))

    def test_get_with_none(self):
        system = {'a': None}
        event = self._makeOne(system)
        self.assertIsNone(event.get('a'))

    def test_get_multiple_keys(self):
        system = {'a': 1, 'b': 2, 'c': 3}
        event = self._makeOne(system)
        self.assertEqual(event.get('a'), 1)
        self.assertEqual(event.get('b'), 2)
        self.assertEqual(event.get('c'), 3)

    def test_get_with_numeric_key(self):
        system = {1: 'one', 2: 'two'}
        event = self._makeOne(system)
        self.assertEqual(event.get(1), 'one')
        self.assertEqual(event.get(2), 'two')
        self.assertIsNone(event.get(3))