import os
import unittest
from pyramid.renderers import null_renderer
from pyramid.response import Response
from pyramid.exceptions import BadCSRFToken
from pyramid.testing import DummyRequest
from pyramid.config import Configurator

class TestView(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)
        self.config.add_view(self.view, require_csrf=True, renderer=null_renderer)

    def view(self, request):
        return 'OK'

    def test_view_with_valid_csrf_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.headers = {'X-CSRF-Token': 'foo'}
        request.session = {'csrf_token': 'foo'}
        response = self.config.make_wsgi_app()(request.environ, start_response=lambda status, headers: None)
        self.assertEqual(response, 'OK')

    def test_view_with_invalid_csrf_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.headers = {'X-CSRF-Token': 'invalid'}
        request.session = {'csrf_token': 'foo'}
        with self.assertRaises(BadCSRFToken):
            self.config.make_wsgi_app()(request.environ, start_response=lambda status, headers: None)

    def test_view_with_no_csrf_token(self):
        request = DummyRequest()
        request.method = 'POST'
        request.headers = {}
        request.session = {'csrf_token': 'foo'}
        with self.assertRaises(BadCSRFToken):
            self.config.make_wsgi_app()(request.environ, start_response=lambda status, headers: None)

    def test_view_with_get_method(self):
        request = DummyRequest()
        request.method = 'GET'
        response = self.config.make_wsgi_app()(request.environ, start_response=lambda status, headers: None)
        self.assertEqual(response, 'OK')

    def test_view_with_empty_post_data(self):
        request = DummyRequest()
        request.method = 'POST'
        request.POST = {}
        request.headers = {'X-CSRF-Token': 'foo'}
        request.session = {'csrf_token': 'foo'}
        response = self.config.make_wsgi_app()(request.environ, start_response=lambda status, headers: None)
        self.assertEqual(response, 'OK')