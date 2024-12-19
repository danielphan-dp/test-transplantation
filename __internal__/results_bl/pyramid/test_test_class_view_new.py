import os
import unittest
from .dummy import DummyView
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_arguments(self):
        self.config.add_route('bar', '/c/d')
        self.assertIn('bar', self.config.routes)
        self.assertEqual(self.config.routes['bar'].pattern, '/c/d')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/e/f')

    def test_add_route_with_none_name(self):
        with self.assertRaises(TypeError):
            self.config.add_route(None, '/g/h')

    def test_add_route_with_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('baz', '')

    def test_add_route_with_multiple_arguments(self):
        self.config.add_route('qux', '/i/j', request_method='GET')
        self.assertIn('qux', self.config.routes)
        self.assertEqual(self.config.routes['qux'].pattern, '/i/j')
        self.assertEqual(self.config.routes['qux'].request_method, ['GET'])

    def test_add_route_with_view(self):
        self.config.add_route('quux', '/k/l')
        self.config.add_view(route_name='quux', view=DummyView, attr='view', renderer=nr)
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()