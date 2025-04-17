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
        # Mock implementation for registering resource URL
        pass

    def test_resource_url_with_default_values(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        root = DummyContext()
        result = self.request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        root = DummyContext()
        result = self.request.resource_url(root, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        root = DummyContext()
        result = self.request.resource_url(root, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_query_and_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, query={'a': '1'}, anchor='section')
        self.assertEqual(result, 'http://example.com:5432/context/?a=1#section')

    def test_resource_url_with_unicode_anchor(self):
        root = DummyContext()
        uc = 'La Peñá'
        result = self.request.resource_url(root, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_empty_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

class DummyContext:
    __name__ = 'context'
    __parent__ = None