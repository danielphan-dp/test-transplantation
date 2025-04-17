import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.request = DummyRequest()
        self.request.registry = self.config.registry

    def test_route_url_with_no_elements(self):
        self.config.add_route('test_route', '/test')
        result = self.request.route_url('test_route')
        self.assertEqual(result, 'http://localhost/test')

    def test_route_url_with_single_element(self):
        self.config.add_route('test_route', '/test/{param}')
        result = self.request.route_url('test_route', 'value')
        self.assertEqual(result, 'http://localhost/test/value')

    def test_route_url_with_multiple_elements(self):
        self.config.add_route('test_route', '/test/{param1}/{param2}')
        result = self.request.route_url('test_route', 'value1', 'value2')
        self.assertEqual(result, 'http://localhost/test/value1/value2')

    def test_route_url_with_query_params(self):
        self.config.add_route('test_route', '/test')
        result = self.request.route_url('test_route', _query={'key': 'value'})
        self.assertEqual(result, 'http://localhost/test?key=value')

    def test_route_url_with_dynamic_route(self):
        from pyramid.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(route=DummyRoute('/dynamic/{param}'))
        self.request.registry.registerUtility(mapper, IRoutesMapper)
        result = self.request.route_url('dynamic', 'value')
        self.assertEqual(result, 'http://localhost/dynamic/value')

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_empty_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('')

    def test_route_url_with_extra_query_params(self):
        self.config.add_route('test_route', '/test')
        result = self.request.route_url('test_route', _query={'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(result, 'http://localhost/test?key1=value1&key2=value2')

if __name__ == '__main__':
    unittest.main()