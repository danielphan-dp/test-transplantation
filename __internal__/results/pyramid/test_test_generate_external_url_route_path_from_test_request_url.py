import unittest
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_name_and_path(self):
        self.config.add_route('test_route', '/test/path')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'test_route')
        self.assertEqual(route[0].pattern, '/test/path')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/test/path')

    def test_add_route_with_empty_path(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('test_route', '')

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('duplicate_route', '/first/path')
        with self.assertRaises(ConfigurationError):
            self.config.add_route('duplicate_route', '/second/path')

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/test/path/{foo}')
        route = self.config.get_routes()
        self.assertEqual(route[0].pattern, '/test/path/{foo}')

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('invalid_route', '/test/{foo}/')

    def test_add_route_with_request_param(self):
        self.config.add_route('param_route', '/param', request_param='abc')
        route = self.config.get_routes()
        self.assertEqual(route[0].name, 'param_route')
        self.assertEqual(route[0].request_param, 'abc')