import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_url_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub')
        self.assertEqual(result, '/1/2/3')

    def test_route_url_with_multiple_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, '/1/2/3/element1/element2')

    def test_route_url_with_query_parameters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, '/1/2/3?key=value')

    def test_route_url_with_anchor(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _anchor='section1')
        self.assertEqual(result, '/1/2/3#section1')

    def test_route_url_with_app_url(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute(result='/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _app_url='http://example.com')
        self.assertEqual(result, 'http://example.com/1/2/3')

    def test_route_url_with_invalid_route(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=None)
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result