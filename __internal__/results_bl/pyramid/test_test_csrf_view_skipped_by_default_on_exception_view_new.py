import unittest
from pyramid.request import Request
from pyramid.response import Response

class TestGetResponseMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()

    def test_get_response_returns_app(self):
        app = self.config.make_wsgi_app()
        response = self.config.get_response(app)
        self.assertIs(response, app)

    def test_get_response_with_invalid_app(self):
        with self.assertRaises(TypeError):
            self.config.get_response(None)

    def test_get_response_with_custom_app(self):
        class CustomApp:
            pass
        
        custom_app = CustomApp()
        response = self.config.get_response(custom_app)
        self.assertIs(response, custom_app)

    def test_get_response_with_different_request_methods(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        request.method = 'GET'
        response = request.get_response(app)
        self.assertEqual(response.status_code, 200)

    def test_get_response_with_post_request(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        request.method = 'POST'
        response = request.get_response(app)
        self.assertEqual(response.status_code, 200)