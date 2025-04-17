import os
import unittest
from pyramid.interfaces import IRoutesMapper
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        environ = {'wsgi.url_scheme': 'http', 'SERVER_PORT': '5432'}
        self.request = DummyRequest(environ)
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_host(self):
        result = self.request.route_url('flub', _host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/1/2/3')

    def test_route_url_with_no_host(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://localhost:5432/1/2/3')

    def test_route_url_with_additional_elements(self):
        result = self.request.route_url('flub', 'extra', 'path')
        self.assertEqual(result, 'http://localhost:5432/1/2/3/extra/path')

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://localhost:5432/1/2/3?key=value')

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