import unittest
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        return registry

    def test_resource_url_with_default_values(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://customurl.com')
        self.assertEqual(result, 'http://customurl.com/context/')

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

    def test_resource_url_with_invalid_app_url(self):
        root = DummyContext()
        with self.assertRaises(ValueError):
            self.request.resource_url(root, app_url='invalid-url')

    def test_resource_url_with_empty_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_unicode_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='La Peña')
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_query_params(self):
        root = DummyContext()
        result = self.request.resource_url(root, query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?key=value')

class DummyContext:
    __name__ = 'context'
    __parent__ = None