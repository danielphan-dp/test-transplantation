import os
import unittest
from pyramid.testing import DummyRequest, DummyRoute
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_route_url_with_no_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub')
        self.assertEqual(result, '/')

    def test_route_url_with_multiple_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, '/1/2/3/element1/element2')

    def test_route_url_with_query_string(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, '/1/2/3?key=value')

    def test_route_url_with_empty_query_string(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={})
        self.assertEqual(result, '/1/2/3')

    def test_route_url_with_invalid_route_name(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result=None))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(ValueError):
            self.request.route_url('invalid_route')

    def test_route_url_with_anchor(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _anchor='section')
        self.assertEqual(result, '/1/2/3#section')

    def test_route_url_with_app_url(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _app_url='http://example.com')
        self.assertEqual(result, 'http://example.com/1/2/3')

    def test_route_url_with_app_url_and_query(self):
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _app_url='http://example.com', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com/1/2/3?key=value')