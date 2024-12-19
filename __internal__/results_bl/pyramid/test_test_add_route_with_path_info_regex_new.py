import unittest
from pyramid.util import text_
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def _assertRoute(self, config, name, path, expected_count):
        routes = config.get_routes_mapper().get_routes()
        self.assertEqual(len(routes), expected_count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        return DummyRequest(config)

    def test_add_route_with_empty_path(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', '')
        route = self._assertRoute(config, 'name', '', 1)
        self.assertEqual(route.path, '')

    def test_add_route_with_special_characters(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path_with_special_@#')
        route = self._assertRoute(config, 'name', 'path_with_special_@#', 1)
        self.assertEqual(route.path, 'path_with_special_@#')

    def test_add_route_with_multiple_arguments(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', method='GET', request_method='POST')
        route = self._assertRoute(config, 'name', 'path', 1)
        self.assertIn('GET', route.methods)
        self.assertIn('POST', route.methods)

    def test_add_route_with_none_name(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(ConfigurationError):
            config.add_route(None, 'path')

    def test_add_route_with_none_path(self):
        config = self._makeOne(autocommit=True)
        with self.assertRaises(ConfigurationError):
            config.add_route('name', None)

class DummyRequest:
    def __init__(self, config):
        self.config = config
        self.upath_info = ''