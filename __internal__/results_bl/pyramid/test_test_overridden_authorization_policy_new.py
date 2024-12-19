import unittest
from pyramid.config import Configurator
from webtest import TestApp

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        config = Configurator()
        self.app = config.make_wsgi_app()
        self.testapp = TestApp(self.app)

    def test_get_method_returns_cookie(self):
        response = self.testapp.get('/some_endpoint', status=200)
        self.assertIn('Set-Cookie', response.headers)

    def test_get_method_with_invalid_name(self):
        response = self.testapp.get('/some_invalid_endpoint', status=404)
        self.assertEqual(response.status_code, 404)

    def test_get_method_without_cookie(self):
        response = self.testapp.get('/some_endpoint_without_cookie', status=200)
        self.assertNotIn('Set-Cookie', response.headers)

    def test_get_method_with_empty_name(self):
        response = self.testapp.get('/some_endpoint?name=', status=200)
        self.assertIn('Set-Cookie', response.headers)

    def test_get_method_with_special_characters(self):
        response = self.testapp.get('/some_endpoint?name=%40%23%24%25', status=200)
        self.assertIn('Set-Cookie', response.headers)