import os
import unittest
from webob.multidict import GetDict
from pyramid.interfaces import IRoutesMapper

class TestCurrentRouteUrl(unittest.TestCase):
    def _makeOne(self):
        from pyramid.request import Request
        return Request(environ={'REQUEST_METHOD': 'GET', 'PATH_INFO': '/1/2/3'})

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

    def test_current_route_url_with_single_query_entry(self):
        request = self._makeOne()
        request.GET = GetDict([('key', 'value')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_current_route_url_with_query_override_and_empty_query(self):
        request = self._makeOne()
        request.GET = GetDict([], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url(_query={'new_key': 'new_value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?new_key=new_value')

    def test_current_route_url_with_special_characters_in_query(self):
        request = self._makeOne()
        request.GET = GetDict([('key with space', 'value&value2')], {})
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        request.matched_route = route
        request.matchdict = {}
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key%20with%20space=value%26value2')