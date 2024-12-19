import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        environ = {'wsgi.url_scheme': 'http', 'SERVER_PORT': '5432'}
        self.request = DummyRequest(environ)
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_host(self):
        result = self.request.route_url('flub', _host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/1/2/3')

    def test_route_url_without_host(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'route url')

    def test_route_url_with_empty_elements(self):
        result = self.request.route_url('flub', '')
        self.assertEqual(result, 'route url')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'element1', 'element2')
        self.assertEqual(result, 'route url')

    def test_route_url_with_query_params(self):
        result = self.request.route_url('flub', _query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, 'route url')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_https_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        result = self.request.route_url('flub', _host='securehost.com')
        self.assertEqual(result, 'https://securehost.com:5432/1/2/3')

    def test_route_url_with_custom_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = self.request.route_url('flub', _host='customhost.com')
        self.assertEqual(result, 'http://customhost.com:8080/1/2/3')

    def test_route_url_with_no_elements_and_host(self):
        result = self.request.route_url('flub', _host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:5432/1/2/3')

if __name__ == '__main__':
    unittest.main()