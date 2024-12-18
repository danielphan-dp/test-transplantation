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

    def test_route_url_with_app_url(self):
        result = self.request.route_url('flub', _app_url='http://example2.com')
        self.assertEqual(result, 'http://example2.com/1/2/3')

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'route url')

    def test_route_url_with_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'route url')

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'route url')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')