import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def test_add_route_without_accept_list(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.accept = DummyAccept('application/json')
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_empty_accept_list(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', accept=[])
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.accept = DummyAccept('text/xml')
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_invalid_accept_type(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', accept=['text/xml'])
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.accept = DummyAccept('application/octet-stream')
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_multiple_accept_types(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', accept=['text/xml', 'application/json'])
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.accept = DummyAccept('application/json')
        self.assertEqual(predicate(None, request), True)
        request.accept = DummyAccept('text/xml')
        self.assertEqual(predicate(None, request), True)
        request.accept = DummyAccept('text/html')
        self.assertEqual(predicate(None, request), False)

    def _assertRoute(self, config, name, path, expected_count):
        routes = config.get_routes()
        self.assertEqual(len(routes), expected_count)
        return next(route for route in routes if route.name == name)

    def _makeRequest(self, config):
        class DummyRequest:
            pass
        return DummyRequest()

class DummyAccept:
    def __init__(self, accept_type):
        self.accept = accept_type