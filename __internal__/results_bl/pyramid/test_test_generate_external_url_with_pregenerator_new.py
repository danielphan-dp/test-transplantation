import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import route_url

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', 'https://acme.org/path/{foo}')

    def test_route_url_with_valid_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar'),
            'https://acme.org/path/bar'
        )

    def test_route_url_with_empty_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme'),
            'https://acme.org/path/'
        )

    def test_route_url_with_multiple_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar', baz='qux'),
            'https://acme.org/path/bar'
        )

    def test_route_url_with_query_parameters(self):
        def pregenerator(request, elements, kw):
            kw['_query'] = {'q': 'foo'}
            return elements, kw

        self.config.add_route('acme', 'https://acme.org/path/{foo}', pregenerator=pregenerator)
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar'),
            'https://acme.org/path/bar?q=foo'
        )

    def test_route_url_with_nonexistent_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('nonexistent_route', foo='bar')

    def test_route_url_with_invalid_elements(self):
        request = self.config
        with self.assertRaises(TypeError):
            request.route_url('acme', 123)

    def test_route_url_with_special_characters(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar/baz'),
            'https://acme.org/path/bar/baz'
        )