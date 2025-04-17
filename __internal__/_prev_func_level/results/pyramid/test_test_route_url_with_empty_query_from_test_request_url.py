import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_empty_query(self):
        result = self.request.route_url('flub', _query={})
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', _query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?param=value')

    def test_route_url_with_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/element1/element2')

    def test_route_url_with_dynamic_path_elements(self):
        result = self.request.route_url('flub', foo='1', bar='2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_missing_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('missing_route')

    def test_route_url_with_invalid_elements(self):
        result = self.request.route_url('flub', 'invalid_element')
        self.assertNotEqual(result, 'http://example.com:5432/1/2/3/invalid_element')

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