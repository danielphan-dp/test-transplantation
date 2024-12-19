import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
    
    def test_add_route_with_valid_args(self):
        self.config.add_route('test_route', '/test/{param}')
        self.assertEqual(self.config.route_args, ('test_route',))
        self.assertEqual(self.config.route_kw, {'pattern': '/test/{param}'})

    def test_add_route_with_no_args(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_multiple_args(self):
        self.config.add_route('multi_route', '/multi/{param1}', name='multi')
        self.assertEqual(self.config.route_args, ('multi_route',))
        self.assertEqual(self.config.route_kw, {'pattern': '/multi/{param1}', 'name': 'multi'})

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid_route', None)

    def test_add_route_with_empty_string(self):
        self.config.add_route('empty_route', '')
        self.assertEqual(self.config.route_args, ('empty_route',))
        self.assertEqual(self.config.route_kw, {'pattern': ''})

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/test/{param}@!')
        self.assertEqual(self.config.route_args, ('special_route',))
        self.assertEqual(self.config.route_kw, {'pattern': '/test/{param}@!'})