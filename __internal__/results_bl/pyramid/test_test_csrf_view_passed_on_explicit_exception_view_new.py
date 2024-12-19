import unittest
from pyramid.request import Request
from pyramid.response import Response
from pyramid.exceptions import ConfigurationError

class TestGetResponseMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()

    def test_get_response_with_valid_app(self):
        app = self.config.make_wsgi_app()
        response = self.config.get_response(app)
        self.assertIs(response, app)

    def test_get_response_with_invalid_app(self):
        with self.assertRaises(ConfigurationError):
            self.config.get_response(None)

    def test_get_response_with_custom_app(self):
        class CustomApp:
            pass
        
        app = CustomApp()
        response = self.config.get_response(app)
        self.assertIs(response, app)

    def test_get_response_with_different_app_types(self):
        app = Response('Hello World')
        response = self.config.get_response(app)
        self.assertIs(response, app)

    def test_get_response_with_empty_app(self):
        app = ''
        response = self.config.get_response(app)
        self.assertIs(response, app)