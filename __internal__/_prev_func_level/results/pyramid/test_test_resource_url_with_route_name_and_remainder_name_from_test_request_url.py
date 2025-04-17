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

    def test_resource_url_with_no_registry(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        del request.registry
        root = DummyContext()
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_query_params(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?param=value')

    def test_resource_url_with_empty_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_none_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')