import os
import unittest
from .dummy import DummyBootstrap
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route()
        self.assertEqual(command.route_args, ())
        self.assertEqual(command.route_kw, {})

    def test_add_route_with_only_name(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route('bar')
        self.assertEqual(command.route_args, ('bar',))
        self.assertEqual(command.route_kw, {})

    def test_add_route_with_name_and_path(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route('baz', '/c/d')
        self.assertEqual(command.route_args, ('baz', '/c/d'))
        self.assertEqual(command.route_kw, {})

    def test_add_route_with_name_path_and_extra_kwargs(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route('qux', '/e/f', request_method='GET')
        self.assertEqual(command.route_args, ('qux', '/e/f'))
        self.assertEqual(command.route_kw, {'request_method': 'GET'})

    def test_add_route_with_multiple_routes(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route('route1', '/path1')
        command.add_route('route2', '/path2', request_method='POST')
        self.assertEqual(command.route_args, ('route2', '/path2'))
        self.assertEqual(command.route_kw, {'request_method': 'POST'})

    def test_add_route_with_invalid_method(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(TypeError):
            command.add_route('invalid_route', '/path', request_method=123)

    def test_add_route_with_empty_name(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(ValueError):
            command.add_route('', '/path')

    def test_add_route_with_none_path(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(ValueError):
            command.add_route('route', None)

if __name__ == '__main__':
    unittest.main()