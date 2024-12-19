import unittest
from pyramid.exceptions import ConfigurationError
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_view(self):
        self.config.add_route('name', '/pattern', view='view_function')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {'view': 'view_function'})

    def test_add_route_with_invalid_view_renderer(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', '/pattern', view_renderer='invalid_renderer')

    def test_add_route_with_no_arguments(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name1', '/pattern1', view='view_function1')
        self.config.add_route('name2', '/pattern2', view='view_function2')
        self.assertEqual(self.config.route_args, ('name2', '/pattern2'))
        self.assertEqual(self.config.route_kw, {'view': 'view_function2'})

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/pattern', view='view_function')

    def test_add_route_with_none_pattern(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', None, view='view_function')