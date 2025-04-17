import unittest
from pyramid.request import Request
from pyramid.url import resource_url
from pyramid.testing import DummyRequest, DummyContext

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.root = DummyContext()
        self.root.__name__ = ''
        self.root.__parent__ = None

    def test_resource_url_with_default_app_url(self):
        result = resource_url(self.root, self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_custom_app_url(self):
        result = resource_url(self.root, self.request, app_url='http://custom.com')
        self.assertEqual(result, 'http://custom.com/context/')

    def test_resource_url_with_scheme(self):
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        result = resource_url(self.root, self.request, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        result = resource_url(self.root, self.request, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        result = resource_url(self.root, self.request, port='9090')
        self.assertEqual(result, 'http://example.com:9090/context/')

    def test_resource_url_with_anchor(self):
        result = resource_url(self.root, self.request, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_no_IResourceURL_registered(self):
        result = resource_url(self.root, self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')