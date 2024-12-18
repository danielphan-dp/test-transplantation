import os
import unittest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
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

    def setUp(self):
        self.request = self._makeOne()
        self.mapper = self.DummyRoutesMapper(route=self.DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def _makeOne(self):
        from pyramid.request import Request
        return Request()

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'route url')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'route url')

    def test_route_url_with_query_string(self):
        result = self.request.route_url('flub', _query='(openlayers)')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?(openlayers)')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_query_string(self):
        result = self.request.route_url('flub', _query='')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?')

    def test_route_url_with_additional_kwargs(self):
        result = self.request.route_url('flub', foo='bar', _query='(openlayers)')
        self.assertEqual(result, 'http://example.com:5432/1/2/3?(openlayers)')