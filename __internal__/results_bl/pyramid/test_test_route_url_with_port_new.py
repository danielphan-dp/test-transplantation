import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def _makeOne(self, environ):
        return DummyRequest(environ)

    def test_route_url_with_no_elements(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub')
        self.assertEqual(result, 'http://example.com:5432/')

    def test_route_url_with_empty_elements(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', '')
        self.assertEqual(result, 'http://example.com:5432/1/2/3/')

    def test_route_url_with_query_params(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _query={'key': 'value'})
        self.assertIn('http://example.com:5432/1/2/3', result)
        self.assertIn('key=value', result)

    def test_route_url_with_invalid_route(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_different_scheme(self):
        environ = {
            'wsgi.url_scheme': 'https',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_url('flub', _port='8080')
        self.assertEqual(result, 'https://example.com:8080/1/2/3')