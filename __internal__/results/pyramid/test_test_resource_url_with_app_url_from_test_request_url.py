import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        return registry

    def test_resource_url_with_default_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_custom_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://customurl.com')
        self.assertEqual(result, 'http://customurl.com/context/')

    def test_resource_url_with_empty_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='')
        self.assertEqual(result, '/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        root = DummyContext()
        result = self.request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        root = DummyContext()
        result = self.request.resource_url(root, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        root = DummyContext()
        result = self.request.resource_url(root, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')

    def test_resource_url_with_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_query_params(self):
        root = DummyContext()
        result = self.request.resource_url(root, query={'param1': 'value1'})
        self.assertEqual(result, 'http://example.com:5432/context/?param1=value1')

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')