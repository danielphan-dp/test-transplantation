import unittest
from pyramid.exceptions import ConfigurationError
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_view_permission(self):
        self.config.add_route('name', '/pattern', view_permission='edit')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {'view_permission': 'edit'})

    def test_add_route_without_view_permission(self):
        self.config.add_route('name', '/pattern')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_invalid_view_permission(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', '/pattern', view_permission='invalid_permission')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', '/pattern', view_permission='edit', another_arg='value')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {'view_permission': 'edit', 'another_arg': 'value'})

    def test_add_route_with_no_arguments(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route()