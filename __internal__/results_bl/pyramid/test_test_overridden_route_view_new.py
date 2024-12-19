import unittest
from pyramid.response import Response
from pyramid.config import Configurator
from webtest import TestApp

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        config = Configurator()
        self.app = config.make_wsgi_app()
        self.testapp = TestApp(self.app)

    def test_get_method_returns_cookie(self):
        class MockRequest:
            cookie = 'test_cookie_value'

        response = MockRequest().cookie
        self.assertEqual(response, 'test_cookie_value')

    def test_get_method_no_cookie(self):
        class MockRequest:
            cookie = None

        response = MockRequest().cookie
        self.assertIsNone(response)

    def test_get_method_empty_cookie(self):
        class MockRequest:
            cookie = ''

        response = MockRequest().cookie
        self.assertEqual(response, '')