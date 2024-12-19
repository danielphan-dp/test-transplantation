import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config import Configurator

class TestViewNotFound(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_view_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header='Host')
        wrapper = self.config.make_wsgi_app()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, None)

    def test_view_not_found_with_empty_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header='Host')
        wrapper = self.config.make_wsgi_app()
        request = self._makeRequest(self.config)
        request.headers = {}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_view_not_found_with_invalid_header(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header='Host')
        wrapper = self.config.make_wsgi_app()
        request = self._makeRequest(self.config)
        request.headers = {'InvalidHeader': 'value'}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def _makeRequest(self, config):
        from pyramid.request import Request
        return Request.blank('/', headers={})

    def _assertNotFound(self, wrapper, *arg):
        self.assertRaises(HTTPNotFound, wrapper, *arg)