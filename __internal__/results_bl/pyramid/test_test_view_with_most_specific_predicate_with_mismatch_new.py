import os
import unittest
from pyramid.config import Configurator
from pyramid.router import Router
from pyramid.renderers import null_renderer as nr

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        self.config.add_route('empty_route')
        self.assertIn('empty_route', self.config.routes)

    def test_add_route_with_single_argument(self):
        self.config.add_route('single_arg_route', '/single')
        self.assertIn('single_arg_route', self.config.routes)
        self.assertEqual(self.config.routes['single_arg_route'].pattern, '/single')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('multi_arg_route', '/multi', request_method='GET')
        self.assertIn('multi_arg_route', self.config.routes)
        self.assertEqual(self.config.routes['multi_arg_route'].pattern, '/multi')
        self.assertEqual(self.config.routes['multi_arg_route'].request_method, ('GET',))

    def test_add_route_with_keyword_arguments(self):
        self.config.add_route('kwarg_route', '/kwarg', factory=lambda req: None)
        self.assertIn('kwarg_route', self.config.routes)
        self.assertEqual(self.config.routes['kwarg_route'].factory, lambda req: None)

    def test_add_route_with_conflicting_names(self):
        self.config.add_route('conflict_route', '/conflict')
        with self.assertRaises(Exception):
            self.config.add_route('conflict_route', '/another_conflict')

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(Exception):
            self.config.add_route('invalid_route', None)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(Exception):
            self.config.add_route('', '/empty_name')

    def test_add_route_with_non_string_name(self):
        with self.assertRaises(Exception):
            self.config.add_route(123, '/non_string_name')

    def test_add_route_with_no_pattern(self):
        with self.assertRaises(Exception):
            self.config.add_route('no_pattern_route')

    def test_add_route_with_mixed_methods(self):
        self.config.add_route('mixed_methods_route', '/mixed', request_method=('GET', 'POST'))
        self.assertIn('mixed_methods_route', self.config.routes)
        self.assertEqual(self.config.routes['mixed_methods_route'].request_method, ('GET', 'POST'))

if __name__ == '__main__':
    unittest.main()