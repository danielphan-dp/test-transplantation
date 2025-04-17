import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', '//acme.org/path/{foo}')
        self.request = DummyRequest()
        self.request.registry = self.config.registry

    def test_generate_external_url_with_valid_foo(self):
        self.assertEqual(
            self.request.route_url('acme', foo='bar'), 'http://acme.org/path/bar'
        )

    def test_generate_external_url_with_missing_foo(self):
        with self.assertRaises(KeyError):
            self.request.route_url('acme')

    def test_generate_external_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route', foo='bar')

    def test_generate_external_url_with_multiple_elements(self):
        self.config.add_route('multi', '//example.com/{foo}/{bar}')
        self.assertEqual(
            self.request.route_url('multi', 'first', 'second'), 'http://example.com/first/second'
        )

    def test_generate_external_url_with_query_params(self):
        self.config.add_route('query', '//example.com/path')
        self.assertEqual(
            self.request.route_url('query', _query={'key': 'value'}),
            'http://example.com/path?key=value'
        )