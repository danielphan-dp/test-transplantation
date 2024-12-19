import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import route_url

class TestRouteUrl(unittest.TestCase):

    def setUp(self):
        self.config = DummyRequest()
        self.config.add_route('acme', '//acme.org/path/{foo}')

    def test_generate_external_url_with_scheme(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar', _scheme='https'), 'https://acme.org/path/bar'
        )

    def test_generate_external_url_with_additional_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', 'extra', foo='bar'), 'http://acme.org/path/bar'
        )

    def test_generate_external_url_with_query_params(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme', foo='bar', _query={'key': 'value'}), 'http://acme.org/path/bar?key=value'
        )

    def test_generate_external_url_without_elements(self):
        request = self.config
        self.assertEqual(
            request.route_url('acme'), 'http://acme.org/path/'
        )

    def test_generate_external_url_with_invalid_route(self):
        request = self.config
        with self.assertRaises(KeyError):
            request.route_url('invalid_route', foo='bar')