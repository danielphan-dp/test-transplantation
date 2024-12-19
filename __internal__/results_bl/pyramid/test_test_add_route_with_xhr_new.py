import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_without_xhr(self):
        self.config.add_route('name', 'path', xhr=False)
        route = self._assertRoute(self.config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(self.config)
        request.is_xhr = False
        self.assertEqual(predicate(None, request), True)
        request.is_xhr = True
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', 'path')

    def test_add_route_with_none_path(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', None)

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'path', xhr=True, custom_arg='value')
        route = self._assertRoute(self.config, 'name', 'path', 1)
        self.assertIn('custom_arg', route.kw)

    def _assertRoute(self, config, name, path, count):
        routes = config.get_routes()
        self.assertEqual(len(routes), count)
        for route in routes:
            if route.name == name and route.path == path:
                return route
        raise AssertionError("Route not found")

    def _makeRequest(self, config):
        class DummyRequest:
            pass
        return DummyRequest()