import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ=self.environ)
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com/1/2/3')

    def test_route_url_with_elements(self):
        result = self.request.route_url('flub', 'extra', 'path')
        self.assertEqual(result, 'http://example.com/1/2/3/extra/path')

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com/1/2/3?key=value')

    def test_route_url_with_scheme_https(self):
        result = self.request.route_url('flub', _scheme='https')
        self.assertEqual(result, 'https://example.com/1/2/3')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_multiple_query_params(self):
        result = self.request.route_url('flub', _query={'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(result, 'http://example.com/1/2/3?key1=value1&key2=value2')

    def test_route_url_with_empty_elements(self):
        result = self.request.route_url('flub', '')
        self.assertEqual(result, 'http://example.com/1/2/3/')

    def test_route_url_with_special_characters(self):
        result = self.request.route_url('flub', 'path with spaces')
        self.assertEqual(result, 'http://example.com/1/2/3/path%20with%20spaces')

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