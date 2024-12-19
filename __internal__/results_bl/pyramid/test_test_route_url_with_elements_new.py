import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_route_url_with_no_elements(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_single_element(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/single'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', 'element1')
        self.assertEqual(result, 'http://example.com:5432/single/element1')

    def test_route_url_with_query_parameters(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/query'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/query?param=value')

    def test_route_url_with_invalid_route(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/valid'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_multiple_query_parameters(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/multiquery'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, 'http://example.com:5432/multiquery?param1=value1&param2=value2')