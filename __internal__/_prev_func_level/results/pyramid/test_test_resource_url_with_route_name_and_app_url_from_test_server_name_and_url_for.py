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
        self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        pass

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://customurl.com')
        self.assertEqual(result, 'http://customurl.com/context/')

    def test_resource_url_with_no_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_invalid_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='invalid-url')
        self.assertEqual(result, 'invalid-url/context/')

    def test_resource_url_with_empty_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='')
        self.assertEqual(result, '/context/')

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

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

class DummyContext:
    __name__ = 'context'
    __parent__ = None