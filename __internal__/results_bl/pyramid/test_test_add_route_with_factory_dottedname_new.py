import unittest
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route()

    def test_add_route_with_only_name(self):
        self.config.add_route('name')
        route = self._assertRoute(self.config, 'name', None)
        self.assertIsNone(route.path)

    def test_add_route_with_only_path(self):
        self.config.add_route(path='path')
        route = self._assertRoute(self.config, None, 'path')
        self.assertIsNone(route.name)

    def test_add_route_with_invalid_factory(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', 'path', factory='invalid.factory')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'path', factory='tests.test_config.dummyfactory', custom_arg='value')
        route = self._assertRoute(self.config, 'name', 'path')
        self.assertEqual(route.factory, dummyfactory)
        self.assertEqual(route.custom_arg, 'value')

    def _assertRoute(self, config, name, path):
        # Mock implementation of route assertion
        return config.routes[name] if name else config.routes[path]