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

    def test_current_route_url_with_query_multiple_keys(self):
        request = self._makeOne()
        request.GET = GetDict([('key1', 'value1'), ('key2', 'value2')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key1=value1&key2=value2')

    def test_current_route_url_with_query_override_and_no_request_query(self):
        request = self._makeOne()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'override_key': 'override_value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?override_key=override_value')

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

    def test_current_route_url_with_query_duplicate_entries(self):
        request = self._makeOne()
        request.GET = GetDict([('q', '123'), ('b', '2'), ('b', '2'), ('q', '456')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?q=123&b=2&b=2&q=456')