import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.context = DummyContext()

    def test_resource_url_with_default_app_url(self):
        result = self.request.resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_custom_app_url(self):
        result = self.request.resource_url(self.context, app_url='http://custom.com')
        self.assertEqual(result, 'http://custom.com/context/')

    def test_resource_url_with_scheme(self):
        result = self.request.resource_url(self.context, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = self.request.resource_url(self.context, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = self.request.resource_url(self.context, port='8080')
        self.assertEqual(result, 'http://example.com:8080/context/')

    def test_resource_url_with_anchor(self):
        result = self.request.resource_url(self.context, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        result = self.request.resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_invalid_context(self):
        with self.assertRaises(Exception):
            self.request.resource_url(None)

    def test_resource_url_with_empty_app_url(self):
        result = self.request.resource_url(self.context, app_url='')
        self.assertEqual(result, '/context/')