import os
import unittest
from pyramid.testing import DummyRequest, DummyContext
from pyramid.interfaces import IRoutesMapper

class TestResourceUrl(unittest.TestCase):

    def _makeOne(self, environ=None):
        request = DummyRequest(environ)
        return request

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        pass

    def test_resource_url_with_virtual_path(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        root.virtual_path = '/context/'
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_invalid_app_url(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, app_url='invalid-url')
        self.assertNotEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_no_registry(self):
        request = self._makeOne()
        del request.registry
        root = DummyContext()
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')