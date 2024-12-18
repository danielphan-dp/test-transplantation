import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = {}
        self.context = DummyContext()

    def test_resource_url_with_no_anchor(self):
        result = resource_url(self.context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_empty_anchor(self):
        result = resource_url(self.context, request=self.request, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_special_characters_in_anchor(self):
        special_anchor = 'test@#&*'
        result = resource_url(self.context, request=self.request, anchor=special_anchor)
        self.assertEqual(result, 'http://example.com:5432/context/#test%40%23%26%2A')

    def test_resource_url_with_unicode_anchor(self):
        unicode_anchor = text_(b'El Ni\xc3\xb1o', 'utf-8')
        result = resource_url(self.context, request=self.request, anchor=unicode_anchor)
        self.assertEqual(result, 'http://example.com:5432/context/#El%20Ni%C3%B1o')

    def test_resource_url_with_app_url(self):
        app_url = 'http://custom-url.com'
        result = resource_url(self.context, request=self.request, app_url=app_url)
        self.assertEqual(result, 'http://custom-url.com/context/')

    def test_resource_url_with_invalid_app_url(self):
        app_url = 'invalid-url'
        result = resource_url(self.context, request=self.request, app_url=app_url)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.context, request=self.request, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.context, request=self.request, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.context, request=self.request, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')