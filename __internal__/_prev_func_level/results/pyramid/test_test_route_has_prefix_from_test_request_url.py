import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', '/foo')

    def test_route_url_with_no_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme'), 'http://localhost/foo')

    def test_route_url_with_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar'), 'http://localhost/foo/bar')

    def test_route_url_with_query_params(self):
        request = self.config
        self.assertEqual(request.route_url('acme', foo='bar'), 'http://localhost/foo?foo=bar')

    def test_route_url_with_route_prefix(self):
        with self.config.route_prefix_context('bar'):
            request = self.config
            self.assertEqual(request.route_url('acme'), 'http://localhost/bar/foo')

    def test_route_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_multiple_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar', 'baz'), 'http://localhost/foo/bar/baz')