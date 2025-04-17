import os
import unittest
from webob.multidict import GetDict
from pyramid.interfaces import IRoutesMapper

class TestCurrentRouteUrl(unittest.TestCase):

    def _makeOne(self):
        from pyramid.request import Request
        return Request.blank('/')

    def test_current_route_url_with_empty_query(self):
        request = self._makeOne()
        request.GET = GetDict([], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_single_query_param(self):
        request = self._makeOne()
        request.GET = GetDict([('key', 'value')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_current_route_url_with_multiple_query_params(self):
        request = self._makeOne()
        request.GET = GetDict([('key1', 'value1'), ('key2', 'value2')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key1=value1&key2=value2')

    def test_current_route_url_with_query_params_and_override(self):
        request = self._makeOne()
        request.GET = GetDict([('key', 'value')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'override_key': 'override_value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?override_key=override_value')

    def test_current_route_url_with_no_route(self):
        request = self._makeOne()
        request.GET = GetDict([], {})
        request.matched_route = None
        request.matchdict = {}
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/')  # Assuming base URL behavior

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route