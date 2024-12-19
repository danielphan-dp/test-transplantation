import os
import unittest
from .dummy import DummyBootstrap
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_view(self):
        self.config.add_route('bar', '/c/d', request_method='GET', view='my_view')
        command = PRoutesCommand()
        L = []
        command.out = L.append
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 3)
        compare_to = L[-1].split()
        expected = ['bar', '/c/d', 'my_view', 'GET']
        self.assertEqual(compare_to, expected)

    def test_add_route_without_method(self):
        self.config.add_route('baz', '/e/f')
        command = PRoutesCommand()
        L = []
        command.out = L.append
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 3)
        compare_to = L[-1].split()
        expected = ['baz', '/e/f', '<unknown>', '<any>']
        self.assertEqual(compare_to, expected)

    def test_add_route_with_multiple_methods(self):
        self.config.add_route('qux', '/g/h', request_method='PUT, DELETE')
        command = PRoutesCommand()
        L = []
        command.out = L.append
        command.bootstrap = DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 3)
        compare_to = L[-1].split()
        expected = ['qux', '/g/h', '<unknown>', 'PUT, DELETE']
        self.assertEqual(compare_to, expected)

    def test_add_route_invalid_method(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid', '/i/j', request_method='INVALID_METHOD')

    def test_add_route_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/k/l')