import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', '/foo')

    def test_route_url_with_no_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme'), 'route url')

    def test_route_url_with_elements(self):
        request = self.config
        self.assertEqual(request.route_url('acme', 'element1', 'element2'), 'route url')

    def test_route_url_with_query_params(self):
        request = self.config
        self.assertEqual(request.route_url('acme', query={'param1': 'value1'}), 'route url')

    def test_route_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route')

    def test_route_url_with_prefix(self):
        with self.config.route_prefix_context('bar'):
            request = self.config
            self.assertEqual(request.route_url('acme'), 'http://localhost/bar/foo')