import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self):
        request = DummyRequest()
        return request

    def test_route_url_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_single_element(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra1')
        self.assertEqual(result, 'http://example.com:5432/1/extra1')

    def test_route_url_with_multiple_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra1', 'extra2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_route_url_with_query_parameters(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', 'extra1', 'extra2', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2?key=value')

    def test_route_url_with_invalid_route(self):
        request = self._makeOne()
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

class DummyRoutesMapper:
    def __init__(self, route=None):
        self.route = route

    def get_route(self, route_name):
        return self.route

class DummyRoute:
    def __init__(self, result='/'):
        self.result = result

    def generate(self, kw):
        return self.result

    @property
    def name(self):
        return 'route'