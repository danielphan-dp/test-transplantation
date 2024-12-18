import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def _makeOne(self, environ=None):
        return DummyRequest(environ)

    def _registerResourceURL(self, registry):
        pass  # Mock implementation for the test

    def test_resource_url_with_no_context(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        result = request.resource_url(None)
        self.assertEqual(result, 'http://example.com:5432/')

    def test_resource_url_with_empty_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, app_url='http://customurl.com')
        self.assertEqual(result, 'http://customurl.com/context/')

    def test_resource_url_with_invalid_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor='invalid anchor')
        self.assertEqual(result, 'http://example.com:5432/context/#invalid%20anchor')

    def test_resource_url_with_scheme_override(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host_override(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:8080/context/')

    def test_resource_url_with_port_override(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')