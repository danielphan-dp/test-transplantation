import os
import unittest
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.interfaces import IRouteRequest, IView, IViewClassifier
from zope.interface import Interface

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

    def test_add_route_with_none_pattern(self):
        with self.assertRaises(ValueError):
            self.config.add_route('baz', None)

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('qux', '/g/h')
        with self.assertRaises(ValueError):
            self.config.add_route('qux', '/i/j')

    def test_add_route_with_view(self):
        def view2(context, request):  # pragma: no cover
            return 'view2'

        self.config.add_route('quux', '/k/l')
        self.config.add_view(route_name='quux', view=view2, renderer=nr)
        self.assertIn('quux', self.config.views)
        self.assertEqual(self.config.views['quux'].view, view2)

    def test_add_route_with_invalid_request_method(self):
        self.config.add_route('corge', '/m/n')
        with self.assertRaises(ValueError):
            self.config.add_view(route_name='corge', view=lambda x, y: None, request_method='INVALID')

    def test_add_route_with_multiple_methods(self):
        self.config.add_route('grault', '/o/p')
        self.config.add_view(route_name='grault', view=lambda x, y: None, request_method=['GET', 'POST'])
        self.assertIn('grault', self.config.views)
        self.assertEqual(self.config.views['grault'].request_method, ['GET', 'POST'])