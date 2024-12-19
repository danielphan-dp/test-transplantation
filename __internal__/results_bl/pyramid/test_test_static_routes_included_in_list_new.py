import os
import unittest
from .dummy import DummyBootstrap
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_parameters(self):
        self.config.add_route('test_route', '/test', static=True)
        self.assertIn('test_route', self.config.routes)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/test', static=True)

    def test_add_route_with_none_name(self):
        with self.assertRaises(TypeError):
            self.config.add_route(None, '/test', static=True)

    def test_add_route_with_invalid_static(self):
        self.config.add_route('invalid_static', '/invalid', static='not_a_bool')
        self.assertIn('invalid_static', self.config.routes)

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('multi_arg', '/multi', static=True, custom_kw='value')
        self.assertIn('multi_arg', self.config.routes)
        self.assertEqual(self.config.routes['multi_arg'].static, True)
        self.assertEqual(self.config.routes['multi_arg'].custom_kw, 'value')

    def test_add_route_with_conflicting_names(self):
        self.config.add_route('conflict', '/conflict', static=True)
        with self.assertRaises(ValueError):
            self.config.add_route('conflict', '/another_conflict', static=True)

    def test_add_route_with_special_characters(self):
        self.config.add_route('special@route!', '/special', static=True)
        self.assertIn('special@route!', self.config.routes)

    def test_add_route_with_long_name(self):
        long_name = 'a' * 256
        with self.assertRaises(ValueError):
            self.config.add_route(long_name, '/long', static=True)

    def test_add_route_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('empty_path', '', static=True)

    def test_add_route_with_non_string_path(self):
        with self.assertRaises(TypeError):
            self.config.add_route('non_string_path', 123, static=True)