import unittest
from pyramid.config import Configurator
from pyramid.response import Response
from webtest import TestApp

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.add_route('get_cookie', '/cookie')
        self.config.add_view(self.get_cookie_view, route_name='get_cookie')
        app = self.config.make_wsgi_app()
        self.testapp = TestApp(app)

    def get_cookie_view(self):
        return Response('Cookie Value')

    def test_get_cookie(self):
        res = self.testapp.get('/cookie', status=200)
        self.assertEqual(res.text, 'Cookie Value')

    def test_get_nonexistent(self):
        res = self.testapp.get('/nonexistent', status=404)
        self.assertIn(b'Not Found', res.body)

    def test_get_empty_name(self):
        res = self.testapp.get('/cookie', status=200)
        self.assertNotEqual(res.text, '')

    def test_get_invalid_name(self):
        with self.assertRaises(Exception):
            self.testapp.get('/invalid', status=400)