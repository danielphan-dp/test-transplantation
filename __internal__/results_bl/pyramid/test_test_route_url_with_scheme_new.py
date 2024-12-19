import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)

    def test_route_url_without_scheme(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://example.com/1/2/3')

    def test_route_url_with_invalid_route(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/{elem}'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', 'test')
        self.assertEqual(result, 'http://example.com/1/2/3/test')

    def test_route_url_with_query_params(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', _query={'key': 'value'})
        self.assertEqual(result, 'http://example.com/1/2/3?key=value')

    def test_route_url_with_empty_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', '')
        self.assertEqual(result, 'http://example.com/1/2/3/')

    def test_route_url_with_multiple_elements(self):
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3/{elem1}/{elem2}'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('flub', 'test1', 'test2')
        self.assertEqual(result, 'http://example.com/1/2/3/test1/test2')