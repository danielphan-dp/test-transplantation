import os
import unittest
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_arguments(self):
        self.config.add_route('bar', '/c/d')
        self.assertEqual(self.config.route_args, ('bar', '/c/d'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/c/d')

    def test_add_route_with_none_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route(None, '/c/d')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('baz', '')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('qux', '/e/f', request_method='GET')
        self.assertEqual(self.config.route_args, ('qux', '/e/f'))
        self.assertEqual(self.config.route_kw, {'request_method': 'GET'})

    def test_add_route_with_conflicting_route(self):
        self.config.add_route('foo', '/a/b')
        with self.assertRaises(ConfigurationError):
            self.config.add_route('foo', '/x/y')

    def test_add_route_with_extra_keywords(self):
        self.config.add_route('quux', '/g/h', custom_kw='value')
        self.assertEqual(self.config.route_kw['custom_kw'], 'value')