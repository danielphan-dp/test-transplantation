import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_no_arguments(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_only_name(self):
        self.config.add_route('name')
        self.assertEqual(self.config.route_args, ('name',))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_and_path(self):
        self.config.add_route('name', 'path')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_path_and_extra_kw(self):
        self.config.add_route('name', 'path', custom_kw='value')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {'custom_kw': 'value'})

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('name', 'path', 'extra_arg')
        self.assertEqual(self.config.route_args, ('name', 'path', 'extra_arg'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_invalid_arguments(self):
        with self.assertRaises(TypeError):
            self.config.add_route('name', 'path', 'extra_arg', 'another_extra_arg', 'too_many_args')