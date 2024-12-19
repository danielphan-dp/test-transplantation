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
        self.command = PRoutesCommand()
        self.command.bootstrap = DummyBootstrap(registry=self.config.registry)

    def test_add_route_with_no_methods(self):
        self.config.add_route('bar', '/c/d')
        L = []
        self.command.out = L.append
        result = self.command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 1)
        compare_to = L[-1].split()
        expected = ['bar', '/c/d', '', '']
        self.assertEqual(compare_to, expected)

    def test_add_route_with_multiple_methods(self):
        self.config.add_route('baz', '/e/f', request_method='GET, POST')
        L = []
        self.command.out = L.append
        result = self.command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 1)
        compare_to = L[-1].split()
        expected = ['baz', '/e/f', '', 'GET, POST']
        self.assertEqual(compare_to, expected)

    def test_add_route_with_invalid_method(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid', '/g/h', request_method='INVALID')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/i/j')

    def test_add_route_with_none_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('none_path', None)

    def test_add_route_with_special_characters(self):
        self.config.add_route('special', '/k/l@#$', request_method='PUT')
        L = []
        self.command.out = L.append
        result = self.command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 1)
        compare_to = L[-1].split()
        expected = ['special', '/k/l@#$', '', 'PUT']
        self.assertEqual(compare_to, expected)