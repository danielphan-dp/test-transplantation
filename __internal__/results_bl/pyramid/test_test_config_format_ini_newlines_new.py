import os
import unittest
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IView
from pyramid.interfaces import IViewClassifier
from pyramid.urldispatch import RoutesMapper
from .dummy import DummyBootstrap, DummyLoader

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_basic(self):
        self.config.add_route('test_route', '/test')
        self.assertIn('test_route', self.config.routes)

    def test_add_route_with_args(self):
        self.config.add_route('test_route_with_args', '/test/{id}')
        self.assertIn('test_route_with_args', self.config.routes)

    def test_add_route_with_kw(self):
        self.config.add_route('test_route_with_kw', '/test', request_method='GET')
        route = self.config.routes['test_route_with_kw']
        self.assertEqual(route.request_method, ['GET'])

    def test_add_route_no_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/no_name')

    def test_add_route_no_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('no_path', '')

    def test_add_route_duplicate_name(self):
        self.config.add_route('duplicate_route', '/duplicate')
        with self.assertRaises(ValueError):
            self.config.add_route('duplicate_route', '/another_duplicate')

    def test_add_route_with_invalid_method(self):
        self.config.add_route('invalid_method_route', '/invalid', request_method='INVALID')
        route = self.config.routes['invalid_method_route']
        self.assertEqual(route.request_method, ['INVALID'])

    def test_add_route_with_multiple_methods(self):
        self.config.add_route('multi_method_route', '/multi', request_method='GET, POST')
        route = self.config.routes['multi_method_route']
        self.assertEqual(route.request_method, ['GET', 'POST'])