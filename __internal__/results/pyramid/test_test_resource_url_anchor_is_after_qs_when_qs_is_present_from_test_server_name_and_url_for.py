import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        return registry

    def test_resource_url_with_no_anchor(self):
        context = DummyContext()
        result = resource_url(context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_empty_anchor(self):
        context = DummyContext()
        result = resource_url(context, anchor='', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_special_characters_in_anchor(self):
        context = DummyContext()
        result = resource_url(context, anchor='!@#$%^&*()', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#!%40%23%24%25%5E%26%2A%28%29')

    def test_resource_url_with_unicode_anchor(self):
        context = DummyContext()
        uc = 'La Peña'
        result = resource_url(context, anchor=uc, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_query_params(self):
        context = DummyContext()
        result = resource_url(context, query={'key': 'value'}, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/?key=value')

    def test_resource_url_with_app_url(self):
        context = DummyContext()
        result = resource_url(context, app_url='http://somewhere.com', request=self.request)
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_custom_scheme(self):
        context = DummyContext()
        result = resource_url(context, scheme='https', request=self.request)
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_custom_host(self):
        context = DummyContext()
        result = resource_url(context, host='customhost.com', request=self.request)
        self.assertEqual(result, 'http://customhost.com:5432/context/')

    def test_resource_url_with_custom_port(self):
        context = DummyContext()
        result = resource_url(context, port='8080', request=self.request)
        self.assertEqual(result, 'http://example.com:8080/context/')

    def test_resource_url_with_no_registry_on_request(self):
        del self.request.registry
        context = DummyContext()
        result = resource_url(context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')