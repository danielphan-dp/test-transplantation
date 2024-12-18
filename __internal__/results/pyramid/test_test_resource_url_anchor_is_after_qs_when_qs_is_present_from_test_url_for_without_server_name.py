import unittest
from pyramid.testing import DummyRequest, DummyResource

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.context = DummyResource()

    def test_resource_url_with_no_anchor(self):
        result = self.request.resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_empty_anchor(self):
        result = self.request.resource_url(self.context, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_special_characters_in_anchor(self):
        result = self.request.resource_url(self.context, anchor='!@#$%^&*()')
        self.assertEqual(result, 'http://example.com:5432/context/#!%40%23%24%25%5E%26%2A%28%29')

    def test_resource_url_with_unicode_anchor(self):
        uc = 'La Peñá'
        result = self.request.resource_url(self.context, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_query_params(self):
        result = self.request.resource_url(self.context, query={'key': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?key=value')

    def test_resource_url_with_app_url(self):
        result = self.request.resource_url(self.context, app_url='http://customurl.com')
        self.assertEqual(result, 'http://customurl.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = self.request.resource_url(self.context, scheme='https')
        self.assertEqual(result, 'https://example.com:8080/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = self.request.resource_url(self.context, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = self.request.resource_url(self.context, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')