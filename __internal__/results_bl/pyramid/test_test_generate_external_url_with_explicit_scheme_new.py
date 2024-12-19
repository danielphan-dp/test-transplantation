import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import route_url

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', '//acme.org/path/{foo}')

    def test_generate_external_url_with_explicit_scheme(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar', _scheme='https'),
            'https://acme.org/path/bar',
        )

    def test_generate_external_url_without_scheme(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='baz'),
            '//acme.org/path/baz',
        )

    def test_generate_external_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route', foo='bar')

    def test_generate_external_url_with_multiple_elements(self):
        self.config.add_route('multi', '//example.org/{foo}/{bar}')
        request = self.config
        self.assertEqual(
            request.route_url('multi', 'first', 'second'),
            '//example.org/first/second',
        )

    def test_generate_external_url_with_query_params(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar', _query={'key': 'value'}),
            '//acme.org/path/bar?key=value',
        )

    def test_generate_external_url_with_empty_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme'),
            '//acme.org/path/',
        )