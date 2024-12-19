import unittest
from pyramid.util.text_ import text_
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def _makeOne(self, autocommit=False):
        return Configurator(autocommit=autocommit)

    def _assertRoute(self, config, name, path, count):
        routes = config.get_routes_mapper().get_routes()
        self.assertEqual(len(routes), count)
        return next(route for route in routes if route.name == name and route.path == path)

    def _makeRequest(self, config):
        return DummyRequest(config)

    def test_add_route_with_empty_path(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', '')
        route = self._assertRoute(config, 'name', '', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = text_('/')
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_special_characters(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info=text_(b'/path_with_special_characters_!@#$', 'utf-8'))
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = text_(b'/path_with_special_characters_!@#$', 'utf-8')
        self.assertEqual(predicate(None, request), True)
        request.upath_info = text_(b'/wrong_path', 'utf-8')
        self.assertEqual(predicate(None, request), False)

    def test_add_route_with_none_path_info(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info=None)
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = text_('/')
        self.assertEqual(predicate(None, request), True)

    def test_add_route_with_non_utf8_path_info(self):
        config = self._makeOne(autocommit=True)
        config.add_route('name', 'path', path_info=text_(b'/path_with_non_utf8_\x80', 'utf-8', errors='ignore'))
        route = self._assertRoute(config, 'name', 'path', 1)
        predicate = route.predicates[0]
        request = self._makeRequest(config)
        request.upath_info = text_(b'/path_with_non_utf8_', 'utf-8', errors='ignore')
        self.assertEqual(predicate(None, request), True)
        request.upath_info = text_(b'/another_path', 'utf-8', errors='ignore')
        self.assertEqual(predicate(None, request), False)