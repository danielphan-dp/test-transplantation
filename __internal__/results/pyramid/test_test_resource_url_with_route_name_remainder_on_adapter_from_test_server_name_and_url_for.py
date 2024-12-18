import unittest
from pyramid.request import Request
from pyramid.interfaces import IRoutesMapper

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = Request(environ)
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock implementation of resource URL registration
        return registry

    def test_resource_url_with_default_context(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://custom.com')
        self.assertEqual(result, 'http://custom.com/context/')

    def test_resource_url_with_scheme(self):
        root = DummyContext()
        result = self.request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        root = DummyContext()
        result = self.request.resource_url(root, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        root = DummyContext()
        result = self.request.resource_url(root, port='8080')
        self.assertEqual(result, 'http://example.com:8080/context/')

    def test_resource_url_with_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_query_params(self):
        root = DummyContext()
        result = self.request.resource_url(root, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?param=value')

    def test_resource_url_no_registry(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

class DummyContext:
    __name__ = 'context'
    __parent__ = None