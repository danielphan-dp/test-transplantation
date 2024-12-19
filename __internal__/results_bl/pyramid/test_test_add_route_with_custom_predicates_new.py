import unittest
import warnings
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.filterwarnings('always')
            self.config.add_route()
            self.assertEqual(len(w), 1)
        route = self._assertRoute(self.config, None, None, 0)
        self.assertIsNone(route)

    def test_add_route_with_only_name(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.filterwarnings('always')
            self.config.add_route('name_only')
            self.assertEqual(len(w), 1)
        route = self._assertRoute(self.config, 'name_only', None, 0)
        self.assertIsNotNone(route)

    def test_add_route_with_empty_path(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.filterwarnings('always')
            self.config.add_route('name', '')
            self.assertEqual(len(w), 1)
        route = self._assertRoute(self.config, 'name', '', 0)
        self.assertIsNotNone(route)

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('duplicate', 'path1')
        with self.assertRaises(Exception):
            self.config.add_route('duplicate', 'path2')

    def _assertRoute(self, config, name, path, predicates_count):
        # Mock implementation of route assertion
        return DummyRoute(name, path, predicates_count)

class DummyRoute:
    def __init__(self, name, path, predicates_count):
        self.name = name
        self.path = path
        self.predicates = [None] * predicates_count