import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/1/2/3')

    def test_route_url_with_single_element(self):
        result = self.request.route_url('flub', 'extra1')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'extra1', 'extra2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra1/extra2')

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', 'extra1', foo='bar')
        self.assertIn('foo=bar', result)

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', 'extra@1', 'extra#2')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/extra%401/extra%232')

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