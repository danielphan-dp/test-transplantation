import os
import unittest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = self._makeOne(self.environ)
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def _makeOne(self, environ):
        from pyramid.request import Request
        return Request(environ)

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

    def test_route_url_with_port(self):
        result = self.request.route_url('flub', _port='8080')
        self.assertEqual(result, 'http://example.com:8080/1/2/3')

    def test_route_url_with_scheme(self):
        result = self.request.route_url('flub', _scheme='https')
        self.assertEqual(result, 'https://example.com:5432/1/2/3')

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