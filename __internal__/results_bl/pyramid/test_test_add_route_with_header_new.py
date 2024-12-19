import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_without_header(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_invalid_header(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', header='Invalid-Header')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.headers = {'Host': 'example.com'}
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_multiple_headers(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', header='Host, User-Agent')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.headers = {'Host': 'example.com', 'User-Agent': 'test-agent'}
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_no_headers(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', header='Host')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.headers = {}
        self.assertEqual(predicate(None, request), False)

    def _assertRoute(self, config, name, path, expected_count):
        routes = config.get_routes()
        self.assertEqual(len(routes), expected_count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/')