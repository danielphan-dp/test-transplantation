import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_without_request_param(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_invalid_request_param(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_param='abc')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.params = {'abc': 'invalid'}
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_multiple_request_params(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_param='abc,xyz')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.params = {'abc': '123', 'xyz': '456'}
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_no_params(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_param='abc')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.params = {}
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_empty_string_param(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_param='abc')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.params = {'abc': ''}
        self.assertEqual(predicate(None, request), False)

    def _assertRoute(self, config, name, path, expected_count):
        routes = config.get_routes()
        self.assertEqual(len(routes), expected_count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/')