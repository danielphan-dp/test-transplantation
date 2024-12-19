import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_default(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_https_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'https://example.com/contextabc/')

    def test_resource_url_with_different_port(self):
        self.request.environ['SERVER_PORT'] = '9090'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_info(self):
        invalid_info = {
            'virtual_path': None,
            'physical_path': None,
            'app_url': None
        }
        with self.assertRaises(KeyError):
            resource_url(self.request, invalid_info)

    def test_resource_url_with_empty_info(self):
        empty_info = {}
        with self.assertRaises(KeyError):
            resource_url(self.request, empty_info)