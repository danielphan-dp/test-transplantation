import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def _assertRoute(self, config, name, path, count):
        routes = config.get_routes_mapper().get_routes()
        self.assertEqual(len(routes), count)
        return next(route for route in routes if route.name == name and route.path == path)

    def test_add_route_with_empty_path_info(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info='')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = ''
        self.assertEqual(predicate(None, request), True)
        request.upath_info = '/foo'
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_none_path_info(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info=None)
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = None
        self.assertEqual(predicate(None, request), True)
        request.upath_info = '/foo'
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_special_characters(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info='/foo/bar@!')
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = '/foo/bar@!'
        self.assertEqual(predicate(None, request), True)
        request.upath_info = '/foo/bar'
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_multiple_routes(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name1', 'path1', path_info='/foo')
        config.add_route('name2', 'path2', path_info='/bar')
        route1 = self._assertRoute(config, 'name1', 'path1', 1)
        route2 = self._assertRoute(config, 'name2', 'path2', 2)
        predicate1 = route1.predicates[0]
        predicate2 = route2.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = '/foo'
        self.assertEqual(predicate1(None, request), True)
        self.assertEqual(predicate2(None, request), False)
        request.upath_info = '/bar'
        self.assertEqual(predicate1(None, request), False)
        self.assertEqual(predicate2(None, request), True)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/')