import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from webob.multidict import GetDict

class TestCurrentRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_current_route_url_with_no_elements(self):
        self.request.GET = GetDict()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        self.request.matched_route = route
        self.request.matchdict = {}
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.current_route_url()
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_single_element(self):
        self.request.GET = GetDict([('key', 'value')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        self.request.matched_route = route
        self.request.matchdict = {}
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.current_route_url('element')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_current_route_url_with_multiple_elements(self):
        self.request.GET = GetDict([('key1', 'value1'), ('key2', 'value2')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        self.request.matched_route = route
        self.request.matchdict = {}
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.current_route_url('element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key1=value1&key2=value2')

    def test_current_route_url_with_empty_query(self):
        self.request.GET = GetDict()
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        self.request.matched_route = route
        self.request.matchdict = {}
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.current_route_url('element')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_current_route_url_with_special_characters(self):
        self.request.GET = GetDict([('key', 'value with spaces'), ('key2', 'value&with&special#chars')])
        route = DummyRoute('/1/2/3')
        mapper = DummyRoutesMapper(route=route)
        self.request.matched_route = route
        self.request.matchdict = {}
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.current_route_url('element')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value%20with%20spaces&key2=value%26with%26special%23chars')