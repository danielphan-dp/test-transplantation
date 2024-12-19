import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_with_no_arguments(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_only_name(self):
        self.config.add_route('test_route')
        self.assertEqual(self.config.route_args, ('test_route',))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_and_pattern(self):
        self.config.add_route('test_route', '/test/{id}')
        self.assertEqual(self.config.route_args, ('test_route', '/test/{id}'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_pattern_and_extra_kw(self):
        self.config.add_route('test_route', '/test/{id}', request_method='GET')
        self.assertEqual(self.config.route_args, ('test_route', '/test/{id}'))
        self.assertEqual(self.config.route_kw, {'request_method': 'GET'})

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid_route', None)

    def test_add_route_with_multiple_routes(self):
        self.config.add_route('route_one', '/one')
        self.config.add_route('route_two', '/two')
        self.assertEqual(self.config.route_args, ('route_two', '/two'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_conflicting_names(self):
        self.config.add_route('conflict', '/path')
        with self.assertRaises(ValueError):
            self.config.add_route('conflict', '/another_path')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/path')

    def test_add_route_with_special_characters(self):
        self.config.add_route('test@route!', '/test/{id}')
        self.assertEqual(self.config.route_args, ('test@route!', '/test/{id}'))
        self.assertEqual(self.config.route_kw, {})

if __name__ == '__main__':
    unittest.main()