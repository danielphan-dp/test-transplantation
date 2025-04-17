import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest, DummyResource

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.root = DummyResource()

    def test_resource_url_with_default_values(self):
        result = self.request.resource_url(self.root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = self.request.resource_url(self.root, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        result = request.resource_url(self.root, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        result = request.resource_url(self.root, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        result = request.resource_url(self.root, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_anchor(self):
        result = self.request.resource_url(self.root, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_no_IResourceURL_registered(self):
        self.root.__name__ = ''
        self.root.__parent__ = None
        result = self.request.resource_url(self.root)
        self.assertEqual(result, 'http://example.com:5432/')