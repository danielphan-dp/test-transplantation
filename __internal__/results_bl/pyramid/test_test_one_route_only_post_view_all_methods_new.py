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

    def test_add_route_with_no_methods(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        command.add_route('bar', '/a/c')
        L = []
        command.out = L.append
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 1)
        compare_to = L[-1].split()
        expected = ['bar', '/a/c', 'None', 'None']
        self.assertEqual(compare_to, expected)

    def test_add_route_with_multiple_methods(self):
        def view2(context, request):  # pragma: no cover
            return 'view2'

        self.config.add_route('baz', '/a/d', request_method='GET, POST')
        self.config.add_view(route_name='baz', view=view2, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        L = []
        command.out = L.append
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 1)
        compare_to = L[-1].split()
        expected = ['baz', '/a/d', 'tests.test_scripts.test_proutes.view2', 'GET, POST']
        self.assertEqual(compare_to, expected)

    def test_add_route_with_invalid_method(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(ValueError):
            command.add_route('invalid', '/a/e', request_method='INVALID_METHOD')

    def test_add_route_with_empty_name(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(ValueError):
            command.add_route('', '/a/f', request_method='GET')

    def test_add_route_with_empty_path(self):
        command = PRoutesCommand()
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        with self.assertRaises(ValueError):
            command.add_route('foo', '', request_method='POST')