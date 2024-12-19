import os
import unittest
from pyramid.config import Configurator
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.renderers import null_renderer as nr
from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IView
from pyramid.interfaces import IViewClassifier
from pyramid.urldispatch import RoutesMapper
from zope.interface import Interface
from .dummy import DummyBootstrap

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_args(self):
        self.config.add_route('bar', '/c/d')
        self.assertIn('bar', self.config.routes)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/c/d')

    def test_add_route_with_none_name(self):
        with self.assertRaises(TypeError):
            self.config.add_route(None, '/c/d')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('baz', '')

    def test_add_route_with_multiple_args(self):
        self.config.add_route('qux', '/e/f', request_method='GET')
        self.assertIn('qux', self.config.routes)
        self.assertEqual(self.config.routes['qux'].request_method, 'GET')

    def test_add_route_with_kwargs(self):
        self.config.add_route('quux', '/g/h', request_method='POST', custom_kw='value')
        self.assertIn('quux', self.config.routes)
        self.assertEqual(self.config.routes['quux'].custom_kw, 'value')

    def test_add_route_overwrite(self):
        self.config.add_route('foo', '/a/b')
        self.config.add_route('foo', '/x/y')
        self.assertEqual(self.config.routes['foo'].pattern, '/x/y')

    def test_add_route_with_conflicting_names(self):
        self.config.add_route('foo', '/a/b')
        with self.assertRaises(ValueError):
            self.config.add_route('foo', '/c/d')

    def test_add_route_with_no_args(self):
        with self.assertRaises(TypeError):
            self.config.add_route()

    def test_add_route_with_invalid_method(self):
        self.config.add_route('foo', '/a/b', request_method='INVALID')
        self.assertIn('foo', self.config.routes)
        self.assertEqual(self.config.routes['foo'].request_method, 'INVALID')