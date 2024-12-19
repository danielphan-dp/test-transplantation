import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def _assertRoute(self, config, name, path, expected_count):
        routes = config.get_routes_mapper().get_routes()
        self.assertEqual(len(routes), expected_count)
        for route in routes:
            if route.name == name and route.path == path:
                return route
        self.fail(f"Route with name '{name}' and path '{path}' not found.")

    def test_add_route_with_multiple_methods(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_method=['GET', 'POST'])
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        
        request = self._makeRequest(config)
        request.method = 'GET'
        self.assertEqual(predicate(None, request), True)
        
        request = self._makeRequest(config)
        request.method = 'POST'
        self.assertEqual(predicate(None, request), True)
        
        request = self._makeRequest(config)
        request.method = 'DELETE'
        self.assertEqual(predicate(None, request), False)

    def test_add_route_without_request_method(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        
        request = self._makeRequest(config)
        request.method = 'GET'
        self.assertEqual(predicate(None, request), True)
        
        request = self._makeRequest(config)
        request.method = 'POST'
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_invalid_method(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', request_method='INVALID')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        
        request = self._makeRequest(config)
        request.method = 'GET'
        self.assertEqual(predicate(None, request), False)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/path', environ={'REQUEST_METHOD': 'GET'})