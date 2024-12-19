import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config import Configurator

class TestNotFoundAssertion(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_assert_not_found_with_none(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_param='abc=123')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {'abc': None}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_empty_string(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_param='abc=123')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {'abc': ''}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_missing_param(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_param='abc=123')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_param(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_param='abc=123')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {'abc': 'invalid'}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def _assertNotFound(self, wrapper, *arg):
        self.assertRaises(HTTPNotFound, wrapper, *arg)