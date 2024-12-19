import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', 'https://acme.org/path/{foo}')

    def test_route_url_with_valid_param(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar'), 'https://acme.org/path/bar'
        )

    def test_route_url_with_missing_param(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('acme')

    def test_route_url_with_extra_param(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar', extra='value'), 'https://acme.org/path/bar'
        )

    def test_route_url_with_invalid_route(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(ValueError):
            request.route_url('invalid_route')

    def test_route_url_with_multiple_elements(self):
        self.config.add_route('multi', 'https://example.com/{foo}/{bar}')
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('multi', 'first', 'second'), 'https://example.com/first/second'
        )

    def _makeRequest(self):
        return DummyRequest()