import unittest
from pyramid.exceptions import ConfigurationError
from pyramid.config import Configurator
from .DummyContext import DummyContext

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_view(self):
        self.config.add_route('name', '/pattern', view_context=DummyContext)
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertIn('view_context', self.config.route_kw)

    def test_add_route_with_no_view_context(self):
        self.config.add_route('name', '/pattern')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertNotIn('view_context', self.config.route_kw)

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('name', None)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ConfigurationError):
            self.config.add_route('', '/pattern')

    def test_add_route_with_multiple_args(self):
        self.config.add_route('name', '/pattern', view_context=DummyContext, another_arg='value')
        self.assertEqual(self.config.route_args, ('name', '/pattern'))
        self.assertEqual(self.config.route_kw['another_arg'], 'value')