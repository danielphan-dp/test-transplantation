import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.request = DummyRequest()
        self.mapper = DummyRoutesMapper(route=DummyRoute('/1/2/3'))
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_route_url_with_no_elements(self):
        result = self.request.route_url('flub')
        self.assertEqual(result, 'http://localhost/1/2/3')

    def test_route_url_with_single_element(self):
        result = self.request.route_url('flub', 'extra1')
        self.assertEqual(result, 'http://localhost/1/2/3/extra1')

    def test_route_url_with_multiple_elements(self):
        result = self.request.route_url('flub', 'extra1', 'extra2')
        self.assertEqual(result, 'http://localhost/1/2/3/extra1/extra2')

    def test_route_url_with_query_parameters(self):
        result = self.request.route_url('flub', 'extra1', _query={'key': 'value'})
        self.assertIn('http://localhost/1/2/3/extra1', result)
        self.assertIn('key=value', result)

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route')

    def test_route_url_with_dynamic_path_elements(self):
        self.config.add_route('dynamic_route', '/dynamic/{foo}')
        self.request.registry = self.config.registry
        result = self.request.route_url('dynamic_route', foo='bar')
        self.assertEqual(result, 'http://localhost/dynamic/bar')

    def test_route_url_with_empty_route_name(self):
        with self.assertRaises(KeyError):
            self.request.route_url('')