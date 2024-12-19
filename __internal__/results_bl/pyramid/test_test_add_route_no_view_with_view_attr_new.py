import unittest
from pyramid.exceptions import ConfigurationError
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_args(self):
        self.config.add_route('name', '/pattern')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_view_attr(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', '/pattern', view_attr='abc')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/pattern')

    def test_add_route_with_none_pattern(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', None)

    def test_add_route_with_multiple_patterns(self):
        self.config.add_route('name', '/pattern1', '/pattern2')
        self.assertEqual(self.config.route_args, ('name', '/pattern1', '/pattern2'))

    def test_add_route_with_extra_kwargs(self):
        self.config.add_route('name', '/pattern', view_attr='abc', custom_kw='value')
        self.assertEqual(self.config.route_kw, {'view_attr': 'abc', 'custom_kw': 'value'})