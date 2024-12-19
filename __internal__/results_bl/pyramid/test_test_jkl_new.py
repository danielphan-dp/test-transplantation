import unittest
from pyramid.response import Response
from pyramid.request import Request
from pyramid.config import Configurator

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.request = Request.blank('/')
        self.cookie = 'test_cookie_value'

    def get(self, name):
        return self.cookie

    def test_get_existing_cookie(self):
        result = self.get('cookie_name')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_non_existing_cookie(self):
        result = self.get('non_existing_cookie')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_empty_name(self):
        result = self.get('')
        self.assertEqual(result, 'test_cookie_value')

    def test_get_none_name(self):
        with self.assertRaises(TypeError):
            self.get(None)

    def test_jkl(self):
        self.testapp.get('/jkl', status=404)