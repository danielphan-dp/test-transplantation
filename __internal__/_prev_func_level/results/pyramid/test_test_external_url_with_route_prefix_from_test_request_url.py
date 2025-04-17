import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', '//acme.org/{foo}')
        self.request = DummyRequest()
        self.request.registry = self.config.registry

    def test_route_url_with_valid_parameters(self):
        self.assertEqual(
            self.request.route_url('acme', foo='bar'), 'http://acme.org/bar'
        )

    def test_route_url_with_missing_parameters(self):
        with self.assertRaises(KeyError):
            self.request.route_url('acme')

    def test_route_url_with_extra_parameters(self):
        self.assertEqual(
            self.request.route_url('acme', foo='bar', extra='value'), 'http://acme.org/bar'
        )

    def test_route_url_with_invalid_route(self):
        with self.assertRaises(KeyError):
            self.request.route_url('invalid_route', foo='bar')

    def test_route_url_with_empty_elements(self):
        self.assertEqual(
            self.request.route_url('acme', ''), 'http://acme.org/'
        )

    def test_route_url_with_special_characters(self):
        self.assertEqual(
            self.request.route_url('acme', foo='b@r'), 'http://acme.org/b%40r'
        )