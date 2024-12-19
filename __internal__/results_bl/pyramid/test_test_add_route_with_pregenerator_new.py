import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_without_pregenerator(self):
        self.config.add_route('name', 'pattern')
        route = self._assertRoute(self.config, 'name', 'pattern')
        self.assertIsNone(route.pregenerator)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', 'pattern')

    def test_add_route_with_none_pattern(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', None)

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'pattern', pregenerator='123', another_arg='value')
        route = self._assertRoute(self.config, 'name', 'pattern')
        self.assertEqual(route.pregenerator, '123')
        self.assertEqual(route.another_arg, 'value')

    def _assertRoute(self, config, name, pattern):
        # Mock implementation of route assertion
        return config.routes[name]  # Assuming routes is a dict-like structure

if __name__ == '__main__':
    unittest.main()