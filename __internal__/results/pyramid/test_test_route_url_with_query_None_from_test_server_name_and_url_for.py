import os
import unittest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.request = self._makeOne()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def _makeOne(self):
        from pyramid.request import Request
        return Request()

    def test_route_url_with_query_None(self):
        result = self.request.route_url('flub', a=1, b=2, c=3, _query=None)
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_empty_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_additional_elements(self):
        result = self.request.route_url('flub', 'extra1', 'extra2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', a=1, b=2, _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3?key=value')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

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