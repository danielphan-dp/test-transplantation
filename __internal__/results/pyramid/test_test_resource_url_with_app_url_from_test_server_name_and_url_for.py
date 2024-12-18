import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def _makeOne(self, environ=None):
        return DummyRequest(environ)

    def _registerResourceURL(self, registry):
        pass  # Mock implementation for the test

    def test_resource_url_with_no_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_empty_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, app_url='')
        self.assertEqual(result, '/context/')

    def test_resource_url_with_invalid_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        root = DummyContext()
        with self.assertRaises(ValueError):
            request.resource_url(root, app_url='invalid-url')

    def test_resource_url_with_custom_scheme(self):
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

    def test_resource_url_with_custom_host(self):
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

    def test_resource_url_with_custom_port(self):
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