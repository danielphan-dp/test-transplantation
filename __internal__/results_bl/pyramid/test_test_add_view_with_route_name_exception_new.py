import os
import unittest
from pyramid.config import Configurator
from pyramid.interfaces import IRouteRequest
from pyramid.renderers import null_renderer
from zope.interface import implementedBy

class TestGetRouteRequestIface(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)
        self.config.add_route('bar', '/c/d')

    def test_get_route_request_iface_valid(self):
        request_iface = self.config.registry.getUtility(IRouteRequest, 'bar')
        self.assertIsNotNone(request_iface)

    def test_get_route_request_iface_invalid(self):
        with self.assertRaises(KeyError):
            self.config.registry.getUtility(IRouteRequest, 'invalid_route')

    def test_get_route_request_iface_no_route(self):
        request_iface = self.config.registry.getUtility(IRouteRequest, 'non_existent_route', default=None)
        self.assertIsNone(request_iface)

    def test_get_route_request_iface_multiple_routes(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, route_name='bar', renderer=null_renderer)
        request_iface = self.config.registry.getUtility(IRouteRequest, 'bar')
        self.assertIsNotNone(request_iface)

    def test_get_route_request_iface_with_context(self):
        view = lambda *arg: 'Context OK'
        self.config.add_view(view=view, route_name='bar', context=RuntimeError, renderer=null_renderer)
        request_iface = self.config.registry.getUtility(IRouteRequest, 'bar')
        wrapper = self.config.get_view_callable(request_iface, context=implementedBy(RuntimeError))
        self.assertIsNotNone(wrapper)
        self.assertEqual(wrapper(None, None), 'Context OK')

if __name__ == '__main__':
    unittest.main()