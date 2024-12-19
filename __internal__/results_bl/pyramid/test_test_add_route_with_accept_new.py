import unittest
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_without_accept(self):
        self.config.add_route('name', 'path')
        route = self._assertRoute(self.config, 'name', 'path', 1)
        self.assertIsNotNone(route)

    def test_add_route_with_invalid_accept(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', 'path', accept='invalid/type')

    def test_add_route_with_multiple_accepts(self):
        self.config.add_route('name', 'path', accept='text/xml,text/html')
        route = self._assertRoute(self.config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(self.config)
        request.accept = DummyAccept('text/xml')
        self.assertEqual(predicate(None, request), True)
        request.accept = DummyAccept('text/html')
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_no_arguments(self):
        with self.assertRaises(TypeError):
            self.config.add_route()

    def _assertRoute(self, config, name, path, count):
        routes = config.get_routes()
        self.assertEqual(len(routes), count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        # Mock request creation logic
        class DummyRequest:
            pass
        return DummyRequest()

class DummyAccept:
    def __init__(self, accept):
        self.accept = accept