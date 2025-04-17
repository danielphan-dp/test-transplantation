import unittest
from pyramid.testing import DummyRequest

class TestResourceURL(unittest.TestCase):

    def _makeOne(self, environ=None):
        return DummyRequest(environ)

    def _registerResourceURL(self, registry):
        pass  # Mock implementation

    def test_resource_url_with_no_app_url(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:8080/context/')

    def test_resource_url_with_empty_app_url(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, app_url='')
        self.assertEqual(result, '/context/')

    def test_resource_url_with_invalid_scheme(self):
        environ = {
            'wsgi.url_scheme': 'ftp',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com:8080/context/')

    def test_resource_url_with_custom_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')

    def test_resource_url_with_custom_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, host='customhost.com')
        self.assertEqual(result, 'http://customhost.com:8080/context/')

    def test_resource_url_with_anchor(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, anchor='section1')
        self.assertEqual(result, 'http://example.com:8080/context/#section1')

    def test_resource_url_with_query_params(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        root = DummyContext()
        result = request.resource_url(root, query={'param1': 'value1'})
        self.assertEqual(result, 'http://example.com:8080/context/?param1=value1')