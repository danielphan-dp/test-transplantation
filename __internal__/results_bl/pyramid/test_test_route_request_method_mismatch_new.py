import os
import unittest
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.interfaces import IRouteRequest, IView
from zope.interface import Interface

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_no_arguments(self):
        self.config.add_route('empty_route')
        self.assertIn('empty_route', self.config.routes)

    def test_add_route_with_only_name(self):
        self.config.add_route('single_name')
        self.assertIn('single_name', self.config.routes)

    def test_add_route_with_path(self):
        self.config.add_route('path_route', '/path')
        self.assertIn('path_route', self.config.routes)
        self.assertEqual(self.config.routes['path_route'].pattern, '/path')

    def test_add_route_with_request_method(self):
        self.config.add_route('method_route', '/method', request_method='GET')
        self.assertIn('method_route', self.config.routes)
        self.assertEqual(self.config.routes['method_route'].request_method, 'GET')

    def test_add_route_with_view(self):
        def view(context, request):
            return 'view response'
        
        self.config.add_route('view_route', '/view')
        self.config.add_view(view, route_name='view_route', renderer=nr)
        self.assertIn('view_route', self.config.routes)

    def test_add_route_with_mismatch_request_method(self):
        def view1(context, request):
            return 'view1'
        
        self.config.add_route('foo', '/a/b', request_method='POST')
        self.config.add_view(route_name='foo', view=view1, renderer=nr, request_method='GET')
        
        command = PRoutesCommand()
        L = []
        command.out = L.append
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 3)
        compare_to = L[-1].split()
        expected = [
            'foo',
            '/a/b',
            'tests.test_scripts.test_proutes.view1',
            '<route',
            'mismatch>',
        ]
        self.assertEqual(compare_to, expected)

    def test_add_route_with_invalid_method(self):
        with self.assertRaises(ValueError):
            self.config.add_route('invalid_method_route', '/invalid', request_method='INVALID')

if __name__ == '__main__':
    unittest.main()