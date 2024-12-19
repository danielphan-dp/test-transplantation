import os
import unittest
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from zope.interface import Interface
from pyramid.interfaces import IRouteRequest, IView, IViewClassifier

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.command = PRoutesCommand()

    def test_add_route_with_valid_args(self):
        self.config.add_route('test_route', '/test')
        self.assertIn('test_route', self.config.routes)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/empty')

    def test_add_route_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid_route', '')

    def test_add_route_with_multiple_args(self):
        self.config.add_route('multi_args', '/multi', request_method='GET', custom_arg='value')
        route = self.config.routes['multi_args']
        self.assertEqual(route.path, '/multi')
        self.assertEqual(route.request_method, ['GET'])

    def test_add_route_with_kw_args(self):
        self.config.add_route('kw_route', '/kw', custom_kw='value')
        route = self.config.routes['kw_route']
        self.assertEqual(route.path, '/kw')

    def test_add_route_overwrite_existing(self):
        self.config.add_route('overwrite', '/path')
        self.config.add_route('overwrite', '/new_path')
        route = self.config.routes['overwrite']
        self.assertEqual(route.path, '/new_path')

    def test_add_route_with_none_args(self):
        self.config.add_route(None, '/none')
        self.assertIn(None, self.config.routes)

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/test@123')
        self.assertIn('special_route', self.config.routes)

    def test_add_route_with_long_name(self):
        long_name = 'a' * 256
        self.config.add_route(long_name, '/long')
        self.assertIn(long_name, self.config.routes)

    def tearDown(self):
        self.config = None
        self.command = None

if __name__ == '__main__':
    unittest.main()