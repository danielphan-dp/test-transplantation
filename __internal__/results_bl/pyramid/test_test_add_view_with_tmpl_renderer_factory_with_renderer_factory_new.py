import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

class TestViewFunction(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.request = DummyRequest()

    def test_view_with_none_context(self):
        response = view(None, self.request)
        self.assertIsInstance(response, Response)

    def test_view_with_empty_context(self):
        response = view({}, self.request)
        self.assertIsInstance(response, Response)

    def test_view_with_invalid_request(self):
        with self.assertRaises(ConfigurationError):
            view({}, None)

    def test_view_with_custom_context(self):
        context = {'key': 'value'}
        response = view(context, self.request)
        self.assertIsInstance(response, Response)

    def test_view_with_renderer(self):
        self.config.add_renderer('.pt', lambda _: lambda val, system_vals: 'Rendered Response')
        self.config.add_view(renderer='dummy.pt')
        view_callable = self.config.make_wsgi_app()
        response = view_callable(self.request.environ, self.request)
        self.assertIn(b'Rendered Response', response.body)

    def test_view_with_invalid_renderer(self):
        self.config.add_view(renderer='invalid.pt')
        with self.assertRaises(ConfigurationError):
            view({}, self.request)

if __name__ == '__main__':
    unittest.main()