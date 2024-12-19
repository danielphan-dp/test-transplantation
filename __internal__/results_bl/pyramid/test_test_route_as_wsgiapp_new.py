import os
import unittest
from pyramid.config import Configurator
from pyramid.registry import Registry
from pyramid.interfaces import IRouteRequest, IView
from pyramid.wsgi import wsgiapp2
from .dummy import DummyBootstrap

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_valid_parameters(self):
        self.config.add_route('test_route', '/test', request_method='GET')
        self.assertIn('test_route', self.config.routes)

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/empty', request_method='GET')

    def test_add_route_with_invalid_method(self):
        self.config.add_route('invalid_method', '/invalid', request_method='INVALID')
        self.assertIn('invalid_method', self.config.routes)

    def test_add_route_with_multiple_methods(self):
        self.config.add_route('multi_method', '/multi', request_method=['GET', 'POST'])
        self.assertIn('multi_method', self.config.routes)

    def test_add_route_overwrite_existing(self):
        self.config.add_route('overwrite', '/overwrite', request_method='GET')
        self.config.add_route('overwrite', '/overwrite', request_method='POST')
        self.assertEqual(len(self.config.routes['overwrite'].methods), 2)

    def test_add_route_with_view(self):
        def view(context, request):
            return 'view response'
        
        self.config.add_route('view_route', '/view', request_method='GET')
        self.config.add_view(view=view, route_name='view_route')
        self.assertIn('view_route', self.config.routes)

    def test_add_route_with_wsgi_app(self):
        config1 = Configurator(autocommit=True)
        config1.add_route('foo', '/a/b', request_method='POST')
        config1.add_view(view=lambda c, r: 'view1', route_name='foo')

        config2 = Configurator(autocommit=True)
        config2.add_route('foo', '/a/b', request_method='POST')
        config2.add_view(wsgiapp2(config1.make_wsgi_app()), route_name='foo')

        command = self._makeOne()
        L = []
        command.out = L.append
        command.bootstrap = DummyBootstrap(registry=config2.registry)
        result = command.run()
        self.assertEqual(result, 0)
        self.assertEqual(len(L), 3)
        compare_to = L[-1].split()
        expected = ['foo', '/a/b', '<wsgiapp>', 'POST']
        self.assertEqual(compare_to, expected)

    def _makeOne(self):
        return PRoutesCommand()

if __name__ == '__main__':
    unittest.main()