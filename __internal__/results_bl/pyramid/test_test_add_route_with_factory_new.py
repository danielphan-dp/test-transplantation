import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_without_factory(self):
        self.config.add_route('name', 'path')
        route = self._assertRoute(self.config, 'name', 'path')
        self.assertIsNone(route.factory)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', 'path')

    def test_add_route_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('name', '')

    def test_add_route_with_none_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route(None, 'path')

    def test_add_route_with_none_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('name', None)

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'path', factory=object(), custom_arg='value')
        route = self._assertRoute(self.config, 'name', 'path')
        self.assertEqual(route.custom_arg, 'value')

    def _assertRoute(self, config, name, path):
        # Mock implementation of route assertion
        return config.routes[name]  # Assuming routes is a dict-like structure in Configurator

if __name__ == '__main__':
    unittest.main()