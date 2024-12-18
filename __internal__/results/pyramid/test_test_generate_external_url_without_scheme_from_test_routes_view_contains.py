import unittest
from pyramid.config import Configurator
from pyramid.request import Request

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_with_valid_name_and_path(self):
        self.config.add_route('test_route', '/test/{param}')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'test_route')
        self.assertEqual(route[0].pattern, '/test/{param}')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/test/{param}')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('test_route', '')

    def test_add_route_with_multiple_routes(self):
        self.config.add_route('route_one', '/one')
        self.config.add_route('route_two', '/two')
        routes = self.config.get_routes()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].name, 'route_one')
        self.assertEqual(routes[1].name, 'route_two')

    def test_add_route_with_dynamic_segments(self):
        self.config.add_route('dynamic_route', '/dynamic/{id}')
        request = Request.blank('/dynamic/123')
        match = self.config.get_routes()[0].match(request.path_info)
        self.assertEqual(match['id'], '123')

    def test_add_route_with_query_params(self):
        self.config.add_route('query_route', '/query')
        request = Request.blank('/query?foo=bar')
        match = self.config.get_routes()[0].match(request.path_info)
        self.assertIsNone(match)

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/test/{name}')
        request = Request.blank('/test/La%20Pe%C3%B1a')
        match = self.config.get_routes()[0].match(request.path_info)
        self.assertEqual(match['name'], 'La Peña')