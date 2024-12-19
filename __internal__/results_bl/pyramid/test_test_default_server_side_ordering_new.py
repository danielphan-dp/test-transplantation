import unittest
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.request import Request

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.app = self.config.make_wsgi_app()

    def test_get_method_returns_cookie(self):
        request = Request.blank('/hello')
        request.cookies['test_cookie'] = 'cookie_value'
        response = self.app.get('/hello', request=request)
        self.assertEqual(response.cookies['test_cookie'], 'cookie_value')

    def test_get_method_no_cookie(self):
        request = Request.blank('/hello')
        response = self.app.get('/hello', request=request)
        self.assertNotIn('test_cookie', response.cookies)

    def test_get_method_with_multiple_cookies(self):
        request = Request.blank('/hello')
        request.cookies['cookie1'] = 'value1'
        request.cookies['cookie2'] = 'value2'
        response = self.app.get('/hello', request=request)
        self.assertEqual(response.cookies['cookie1'], 'value1')
        self.assertEqual(response.cookies['cookie2'], 'value2')

    def test_get_method_with_invalid_cookie(self):
        request = Request.blank('/hello')
        request.cookies['invalid_cookie'] = None
        response = self.app.get('/hello', request=request)
        self.assertNotIn('invalid_cookie', response.cookies)

    def test_get_method_with_special_characters_in_cookie(self):
        request = Request.blank('/hello')
        request.cookies['special_cookie'] = 'value_with_special_chars_!@#$%^&*()'
        response = self.app.get('/hello', request=request)
        self.assertEqual(response.cookies['special_cookie'], 'value_with_special_chars_!@#$%^&*()')