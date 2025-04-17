import os
import unittest
from webob.multidict import GetDict
from pyramid.interfaces import IRoutesMapper

class TestCurrentRouteUrl(unittest.TestCase):
    def _makeOne(self):
        from pyramid.request import Request
        return Request()

    def test_current_route_url_with_no_query(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_empty_query(self):
        request = self._makeOne()
        request.GET = GetDict([])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_query_parameters(self):
        request = self._makeOne()
        request.GET = GetDict([('param1', 'value1'), ('param2', 'value2')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param1=value1&param2=value2')

    def test_current_route_url_with_query_override_and_no_request_query(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'override': 'test'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?override=test')

    def test_current_route_url_with_query_override_and_request_query(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'a': 1})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?a=1')

    def test_current_route_url_with_duplicate_query_parameters(self):
        request = self._makeOne()
        request.GET = GetDict([('param', 'value1'), ('param', 'value2')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param=value1&param=value2')

class DummyRoute:
    def __init__(self, result='/1/2/3'):
        self.result = result

    def generate(self, kw):
        return self.result

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route