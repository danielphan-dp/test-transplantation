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

    def test_route_url_with_single_element(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar'), 'http://localhost/foo/bar')

    def test_route_url_with_multiple_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'bar', 'baz'), 'http://localhost/foo/bar/baz')

    def test_route_url_with_query_params(self):
        request = self.config
        self.assertEqual(request.route_url('acme', _query={'key': 'value'}), 'http://localhost/foo?key=value')

    def test_route_url_with_nonexistent_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('nonexistent_route')

    def test_route_url_with_empty_route_name(self):
        request = self.config
        with self.assertRaises(ValueError):
            request.route_url('')

    def test_route_url_with_invalid_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', None), 'http://localhost/foo/None')