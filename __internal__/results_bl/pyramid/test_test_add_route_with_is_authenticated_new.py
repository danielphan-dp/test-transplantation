import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_without_is_authenticated(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_invalid_is_authenticated(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', is_authenticated='invalid')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.is_authenticated = True
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_none_is_authenticated(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', is_authenticated=None)
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.is_authenticated = True
        self.assertEqual(predicate(None, request), True)

    def _assertRoute(self, config, name, path, count):
        routes = config.get_routes()
        self.assertEqual(len(routes), count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        class Request:
            pass
        return Request()