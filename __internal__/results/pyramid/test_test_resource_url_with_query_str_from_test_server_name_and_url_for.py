import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def _makeOne(self, environ=None):
        return DummyRequest(environ)

    def _registerResourceURL(self, registry):
        pass  # Mock implementation for the test

    def test_resource_url_with_no_registry(self):
        request = self._makeOne()
        del request.registry
        context = DummyContext()
        result = request.resource_url(context)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
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

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = self._makeOne(environ)
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_query_string(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?param=value')

    def test_resource_url_with_anchor(self):
        request = self._makeOne()
        self._registerResourceURL(request.registry)
        context = DummyContext()
        result = request.resource_url(context, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_no_IResourceURL_registered(self):
        root = DummyContext()
        root.__name__ = ''
        root.__parent__ = None
        request = self._makeOne()
        request.environ = {}
        result = request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/')