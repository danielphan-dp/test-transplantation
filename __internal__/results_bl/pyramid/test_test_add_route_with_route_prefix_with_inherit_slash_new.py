import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_only_name(self):
        self.config.add_route('name')
        self.assertEqual(self.config.route_args, ('name',))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_and_pattern(self):
        self.config.add_route('name', '/pattern')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_inherit_slash_false(self):
        self.config.add_route('name', '', inherit_slash=False)
        self.assertEqual(self.config.route_args, ('name', ''))
        self.assertEqual(self.config.route_kw, {'inherit_slash': False})

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', '/pattern', request_method='GET', custom_param='value')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw, {'request_method': 'GET', 'custom_param': 'value'})