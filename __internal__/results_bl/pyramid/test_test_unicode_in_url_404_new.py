import unittest
from pyramid.config import Configurator
from pyramid.response import Response

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.cookie_value = 'test_cookie'
        self.config.add_route('test_route', '/test')
        self.request = self.config.make_wsgi_app()

    def test_get_method_returns_cookie(self):
        response = self.request.get('/test')
        self.assertEqual(response.cookie, self.cookie_value)

    def test_get_method_with_non_existent_name(self):
        response = self.request.get('/non_existent')
        self.assertIsNone(response.cookie)

    def test_get_method_with_special_characters(self):
        special_name = 'test@#$%'
        self.config.add_route('special_route', f'/{special_name}')
        response = self.request.get(f'/{special_name}')
        self.assertEqual(response.cookie, self.cookie_value)

    def test_get_method_with_empty_name(self):
        response = self.request.get('/')
        self.assertIsNone(response.cookie)

    def test_get_method_with_unicode_name(self):
        unicode_name = 'avaliação'
        self.config.add_route('unicode_route', f'/{unicode_name}')
        response = self.request.get(f'/{unicode_name}')
        self.assertEqual(response.cookie, self.cookie_value)