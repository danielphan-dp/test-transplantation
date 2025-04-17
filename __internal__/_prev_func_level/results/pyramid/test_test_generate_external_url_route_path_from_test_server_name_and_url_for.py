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

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('duplicate_route', '/first/path')
        self.config.add_route('duplicate_route', '/second/path')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].pattern, '/second/path')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('invalid_route', None)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/path')

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/path/with/special/!@#$%^&*()')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'special_route')
        self.assertEqual(route[0].pattern, '/path/with/special/!@#$%^&*()')

    def test_add_route_with_path_info(self):
        self.config.add_route('path_info_route', '/path/{foo}')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].pattern, '/path/{foo}')

    def test_add_route_with_request_param(self):
        self.config.add_route('request_param_route', '/request', request_param='abc')
        route = self.config.get_routes()
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0].name, 'request_param_route')
        self.assertEqual(route[0].request_param, 'abc')