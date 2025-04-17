import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', '/foo')

    def test_route_url_without_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme'), 'http://localhost/foo')

    def test_route_url_with_single_element(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar'), 'http://localhost/foo/bar')

    def test_route_url_with_multiple_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar', 'baz'), 'http://localhost/foo/bar/baz')

    def test_route_url_with_query_parameters(self):
        request = self.config
        self.assertEqual(request.route_url('acme', _query={'key': 'value'}), 'http://localhost/foo?key=value')

    def test_route_url_with_dynamic_path_elements(self):
        self.config.add_route('dynamic', '/{foo}/{bar}')
        request = self.config
        self.assertEqual(request.route_url('dynamic', foo='1', bar='2'), 'http://localhost/1/2')

    def test_route_url_with_missing_parameters(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('dynamic', foo='1')

    def test_route_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')