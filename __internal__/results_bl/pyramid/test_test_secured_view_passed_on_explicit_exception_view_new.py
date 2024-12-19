import unittest
from pyramid.request import Request
from pyramid.security import NO_PERMISSION_REQUIRED

class TestGetResponseMethod(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self._registerSecurityPolicy(True)

    def _registerSecurityPolicy(self, enabled):
        if enabled:
            self.config.set_security_policy(None)

    def test_get_response_with_valid_app(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        response = request.get_response(app)
        self.assertIsNotNone(response)

    def test_get_response_with_invalid_app(self):
        with self.assertRaises(Exception):
            request = Request.blank('/invalid', base_url='http://example.com')
            response = request.get_response(None)

    def test_get_response_with_no_app(self):
        with self.assertRaises(TypeError):
            request = Request.blank('/foo', base_url='http://example.com')
            response = request.get_response()

    def test_get_response_with_empty_app(self):
        app = ''
        request = Request.blank('/foo', base_url='http://example.com')
        response = request.get_response(app)
        self.assertIsNotNone(response)

    def test_get_response_with_different_http_methods(self):
        app = self.config.make_wsgi_app()
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            request = Request.blank('/foo', base_url='http://example.com', method=method)
            response = request.get_response(app)
            self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()