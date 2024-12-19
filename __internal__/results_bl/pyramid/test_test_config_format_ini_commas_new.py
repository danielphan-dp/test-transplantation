import os
import unittest
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.interfaces import IRouteRequest, IView, IViewClassifier
from zope.interface import Interface
from .dummy import DummyBootstrap, DummyLoader

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_basic(self):
        self.config.add_route('bar', '/c/d')
        self.assertEqual(self.config.route_args, ('bar',))
        self.assertEqual(self.config.route_kw, {'pattern': '/c/d'})

    def test_add_route_with_extra_args(self):
        self.config.add_route('baz', '/e/f', request_method='GET')
        self.assertEqual(self.config.route_args, ('baz',))
        self.assertEqual(self.config.route_kw, {'pattern': '/e/f', 'request_method': 'GET'})

    def test_add_route_no_args(self):
        with self.assertRaises(TypeError):
            self.config.add_route()

    def test_add_route_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid', '')

    def test_add_route_duplicate_name(self):
        self.config.add_route('duplicate', '/g/h')
        with self.assertRaises(ValueError):
            self.config.add_route('duplicate', '/i/j')

    def test_add_route_with_view(self):
        def view2(context, request):
            return 'view2'

        self.config.add_route('foo', '/a/b')
        self.config.add_view(route_name='foo', view=view2, renderer=nr)
        self.assertIn('foo', self.config.views)

    def test_add_route_with_non_callable_view(self):
        with self.assertRaises(TypeError):
            self.config.add_view(route_name='foo', view='not_a_callable', renderer=nr)

    def test_add_route_with_invalid_request_method(self):
        self.config.add_route('foo', '/a/b', request_method='INVALID')
        self.assertEqual(self.config.route_kw['request_method'], 'INVALID')