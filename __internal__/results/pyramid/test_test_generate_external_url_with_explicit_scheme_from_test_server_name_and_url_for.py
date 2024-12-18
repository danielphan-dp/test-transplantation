import os
import unittest
from pyramid.testing import DummyRequest

class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.add_route('acme', '//acme.org/path/{foo}')

    def _makeRequest(self):
        return DummyRequest()

    def test_route_url_with_valid_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar'),
            'http://acme.org/path/bar',
        )

    def test_route_url_with_missing_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        with self.assertRaises(KeyError):
            request.route_url('acme')

    def test_route_url_with_extra_elements(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', 'extra', foo='bar'),
            'http://acme.org/path/bar/extra',
        )

    def test_route_url_with_query_parameters(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar', _query={'q': 'test'}),
            'http://acme.org/path/bar?q=test',
        )

    def test_route_url_with_explicit_scheme(self):
        request = self._makeRequest()
        request.registry = self.config.registry
        self.assertEqual(
            request.route_url('acme', foo='bar', _scheme='https'),
            'https://acme.org/path/bar',
        )